import json
import requests
from config import FORECAST_API_KEY


URL = 'https://api.forecast.io/forecast'


class WeatherForecast:

    def get_forecast_request(self, lat, lng, time):
        request = requests.get('{url}/{key}/{lat},{lng},{time}'.format(
            url=URL,
            key=FORECAST_API_KEY,
            lat=lat,
            lng=lng,
            time=time
        ))
        return request

    def generate_forecast(self, latitude, longitude, time):
        request = self.get_forecast_request(lat=latitude, lng=longitude, time=time)
        return json.loads(request.text)

    @staticmethod
    def check_forecast_api_is_present():
        return bool(FORECAST_API_KEY)
