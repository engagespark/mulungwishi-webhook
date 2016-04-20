from app import mulungwishi_app as url
from flask import render_template, request, url_for
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
    if not Geocode.check_geocode_api_is_present() and WeatherForecast.check_forecast_api_is_present():
        return url_for('page_server_error')

    place = request.args.get('address')
    if not place:
        return 'No address provided.', 400

    geocode = Geocode(address=place)
    is_place_valid = geocode.is_place_query_valid()

    if not is_place_valid:
        return "Sorry, the location you sent in doesn't appear to be valid. Please check and try again. Thanks!", 400

    forecast = WeatherForecast()
    coordinates = geocode.get_coordinates()
    weather_forecast = forecast.generate_forecast(latitude=coordinates['lat'], longitude=coordinates['lng'])
    return display(forecast=weather_forecast)


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


def convert_to_celsius(temp):
    return round((temp - 32) * 5 / 9, 2)


def convert_to_percentage(amount):
    return int(amount * 100)


def display(forecast):
    forecast = forecast['currently']
    return "Temp: {}C / {}F, Humidity: {}%, Precip: {}%, Summary: {}".format(
        convert_to_celsius(forecast['temperature']),
        forecast['temperature'],
        convert_to_percentage(forecast['humidity']),
        convert_to_percentage(forecast['precipProbability']),
        forecast['summary']
    )
