import json
import pytz
import requests
from config import GEOCODE_API_KEY, TIMEZONE_API_KEY
from datetime import datetime


GEOCODE_URL = 'https://maps.googleapis.com/maps/api/geocode/json?'
TIMEZONE_URL = 'https://maps.googleapis.com/maps/api/timezone/json?'


class Geolocation:

    def __init__(self, address):
        self.address = address

    def get_address_query(self):
        params = {'address': self.address, 'key': GEOCODE_API_KEY}
        return json.loads(requests.get(GEOCODE_URL, params=params).text)

    def is_place_query_valid(self):
        status = self.get_address_query()['status']
        return status == 'OK'

    @property
    def coordinates(self):
        geocode_info = self.get_address_query()
        lat = geocode_info['results'][0]['geometry']['location']['lat']
        lng = geocode_info['results'][0]['geometry']['location']['lng']
        return {'lat': lat, 'lng': lng}

    @property
    def local_time(self):
        coordinates = self.coordinates
        timezone_request_params = {
            'location': ','.join(['%s' % value for (key, value) in coordinates.items()]),
            'timestamp': 1331161200,
            'key': TIMEZONE_API_KEY,
        }
        timezone_request = json.loads(requests.get(
            TIMEZONE_URL,
            params=timezone_request_params,
        ).text)
        timezone = timezone_request['timeZoneId']
        tz = pytz.timezone(timezone)
        return datetime.now(tz).strftime('%Y-%m-%dT%H:%M:%S')

    @staticmethod
    def check_geolocation_api_keys_are_present():
        return bool(GEOCODE_API_KEY) and bool(TIMEZONE_API_KEY)
