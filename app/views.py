from .weather_parser import WeatherForecast
from app import mulungwishi_app as url
from flask import render_template, request


@url.route('/')
def index():
    return render_template('index.html')


@url.route('/query')
def show_user_input():
    content = request.args.get('content')
    sms_from = request.args.get('from')
    sms_to = request.args.get('to')

    valid_query_message = "Content: {}  SMS From: {}    SMS To: {}".format(content, sms_from, sms_to)
    invalid_query_message = "You've entered an incorrect/empty query. Please check and try again. You can try '/query?content=sms_content&from=number_it_came_from&to=number_it_will_go_to'"
    invalid_query_status_code = 400

    return valid_query_message if content and sms_from and sms_to else (invalid_query_message, invalid_query_status_code)


@url.route('/weather_forecast')
def generate_forecast():
    forecast = WeatherForecast()
    place = request.args.get('address')
    if not place:
        return 'No address provided.', 400
    query_status = forecast.get_requests(address=place)
    if not isinstance(query_status, str):
        weather_forecast = forecast.generate_forecast(address=place)
        place_info = forecast.get_place_info()
        return 'WEATHER FORECAST FOR {}: \nPlace Type: {}\n{}'.format(place_info['formatted_address'].upper(), place_info['place_type'], display(forecast=weather_forecast))
    return '{}. Try a more generic place name i.e. local, province'.format(weather_forecast), 400


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
    return time.strftime('%a %b %d,%Y %I:%M:%S %p')


def display(forecast):
    return 'Time: {}\nTemperature: {}°C\nHumidity: {}\nProbability of Precipitation: {}\nWeather Summary: {}'.format(convert_to_readable_time(forecast.time), round(forecast.temperature, 2), forecast.humidity, forecast.precipProbability, forecast.summary)
