import json
import requests
from config import GEOCODE_API_KEY


geocode_url = 'https://maps.googleapis.com/maps/api/geocode/json?'


class Geocode:

    def __init__(self, address):
        self.address = address
        self.formatted_address = None
        self.place_type = None

    def get_address_query(self):
        params = {'address': self.address, 'key': GEOCODE_API_KEY}
        return json.loads(requests.get(geocode_url, params=params).text)

    def is_place_query_valid(self):
        status = self.get_address_query()['status']
        return status == 'OK'

    def get_coordinates(self):
        geocode_info = self.get_address_query()
        lat = geocode_info['results'][0]['geometry']['location']['lat']
        lng = geocode_info['results'][0]['geometry']['location']['lng']
        return {'lat': lat, 'lng': lng}

    def get_place_info(self):
        geocode_info = self.get_address_query()
        self.formatted_address = geocode_info['results'][0]['formatted_address']
        self.place_type = geocode_info['results'][0]['address_components'][0]['types'][0]
        return {'place_type': self.place_type, 'formatted_address': self.formatted_address}

    @staticmethod
    def check_geocode_api_is_present():
        return bool(GEOCODE_API_KEY)
