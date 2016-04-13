from app import mulungwishi_app as url
from flask import render_template, request
from .geocode_api_parser import Geocode
from .weather_parser import WeatherForecast


@url.route('/')
def index():
    return render_template('index.html')


@url.route('/query')
def show_user_input():
    content = request.args.get('content')
    sms_from = request.args.get('from')
    sms_to = request.args.get('to')

    valid_query_message = "Content: {}  SMS From: {}    SMS To: {}".format(content, sms_from, sms_to)
    invalid_query_message = "You've entered an incorrect/empty query. Please check and try again.\
                             You can try '/query?content=sms_content&from=number_it_came_from&to=number_it_will_go_to'"
    invalid_query_status_code = 400

    return valid_query_message if content and sms_from and sms_to else (invalid_query_message, invalid_query_status_code)


@url.route('/weather_forecast')
def generate_forecast():
    place = request.args.get('address')
    if not place:
        return 'No address provided.', 400

    frequency = 'currently'  # default forecast set to current
    valid_frequency = ['currently', 'hourly', 'daily']
    last_query = place.split(' ')[-1].lower()
    if last_query in valid_frequency:
        place = place.replace(last_query, '')  # replace time method(if present) with empty string so that only the place remains. Example query: cebu hourly
        frequency = last_query

    geocode = Geocode(address=place)
    is_place_valid = geocode.is_place_query_valid()

    if not is_place_valid:
        return 'No results found. Try a more generic place name i.e. local, province', 400

    forecast = WeatherForecast()
    coordinates = geocode.get_coordinates()
    weather_forecast = forecast.generate_forecast(latitude=coordinates['lat'], longitude=coordinates['lng'], frequency=frequency)
    place_info = geocode.get_place_info()
    return 'WEATHER FORECAST FOR {}: \nPlace Type: {}\n{}'.\
        format(place_info['formatted_address'].upper(), place_info['place_type'], display(forecast=weather_forecast, frequency=frequency))


@url.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


@url.errorhandler(403)
def page_forbidden(error):
    return render_template('403.html', title='Page Forbidden'), 403


@url.errorhandler(500)
def page_server_error(error):
    return render_template('500.html', title='Server Error'), 500


def convert_to_readable_time(time):
    return time.strftime('%a %b %d, %Y %I:%M:%S %p')


def display(forecast, frequency):
    if frequency == 'currently':
        return '{}\nTemperature: {}°C\nHumidity: {}\nProbability of Precipitation: {}\nWeather Summary: {}'.\
            format(convert_to_readable_time(forecast.time), round(forecast.temperature, 2), forecast.humidity, forecast.precipProbability, forecast.summary)

    info = []
    for count, item in enumerate(forecast.data):
        info.append(str(convert_to_readable_time(item.time)))
        if frequency == 'hourly':
            info.append('temperature: ' + str(item.temperature))
        else:
            info.append('temperatureMin: ' + str(item.temperatureMin))
            info.append('temperatureMax: ' + str(item.temperatureMax))
        info.append('humidity: ' + str(item.humidity))
        info.append('precipProbability: ' + str(item.precipProbability))
        info.append('summary: ' + str(item.summary) + '\n')
        if count > 12:
            break
    return '\n'.join(info)
