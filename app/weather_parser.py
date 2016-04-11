import forecastio
import json
import requests
from config import FORECAST_API_KEY, GEOCODE_API_KEY


forecast_api_key = FORECAST_API_KEY
geocode_api_key = GEOCODE_API_KEY
geocode_url = 'https://maps.googleapis.com/maps/api/geocode/json?'
place_type = None
formatted_address = None


class WeatherForecast:

    def __init__(self):
        self.place_type = None
        self.formatted_address = None

    def get_requests(self, address):
        geocodes = self.get_geocode_request(address=address)
        place_query_status = geocodes['status']
        if place_query_status == 'OK':
            self.place_type = geocodes['results'][0]['address_components'][0]['types'][0]
            self.formatted_address = geocodes['results'][0]['formatted_address']
            latitude = geocodes['results'][0]['geometry']['location']['lat']
            longitude = geocodes['results'][0]['geometry']['location']['lng']
            return self.get_forecast_request(latitude=latitude, longitude=longitude)
        return str(place_query_status)

    def generate_forecast(self, address):
        forecast = self.get_requests(address)
        return forecast.currently()

    def get_place_info(self):
        return ({'place_type': self.place_type, 'formatted_address': self.formatted_address})

    def get_geocode_request(self, address):
        return json.loads(requests.get('{}address={}&key={}'.format(geocode_url, address, geocode_api_key)).text)

    def get_forecast_request(self, latitude, longitude):
        return forecastio.load_forecast(forecast_api_key, latitude, longitude)
