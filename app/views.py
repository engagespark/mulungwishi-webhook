import forecastio
from app import mulungwishi_app as url
from config import FORECAST_API_KEY
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


@url.route('/ask_weather')
def generate_forecast():
    query = request.args.get('coordinates')
    if not query:
        return 'No coordinates provided.', 400
    latitude, longitude = query.split(',')
    forecast = forecastio.load_forecast(FORECAST_API_KEY, latitude, longitude).currently()
    return 'Time: {}\nTemperature: {}\nHumidity: {}\nProbability of Precipitation: {}\nSummary: {}'.format(forecast.time.strftime('%I:%M:%S %p'), forecast.temperature, forecast.humidity, forecast.precipProbability, forecast.summary)


@url.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


@url.errorhandler(403)
def page_forbidden(error):
    return render_template('403.html', title='Page Forbidden'), 403


@url.errorhandler(500)
def page_server_error(error):
    return render_template('500.html', title='Server Error'), 500
