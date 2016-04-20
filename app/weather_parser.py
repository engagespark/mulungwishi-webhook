import json
import requests
from config import FORECAST_API_KEY


class WeatherForecast:

    def get_forecast_request(self, lat, lng, time=None):
        url = 'https://api.forecast.io/forecast'
        if not time:
            request = requests.get('{url}/{key}/{lat},{lng}'.format(
                url=url,
                key=FORECAST_API_KEY,
                lat=lat,
                lng=lng
            ))
        else:
            request = requests.get('{url}/{key}/{lat},{lng},{time}'.format(
                url=url,
                key=FORECAST_API_KEY,
                lat=lat,
                lng=lng,
                time=time
            ))
        return request

    def generate_forecast(self, latitude, longitude):
        request = self.get_forecast_request(lat=latitude, lng=longitude)
        return json.loads(request.text)

    @staticmethod
    def check_forecast_api_is_present():
        return bool(FORECAST_API_KEY)
