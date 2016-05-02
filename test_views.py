#!/usr/bin/env python
import json
import unittest
from unittest.mock import patch

# This line is important so flake8 must ignore this one
from app import views # flake8: noqa
from app import mulungwishi_app


class URLTest(unittest.TestCase):

    def setUp(self):
        self.client = mulungwishi_app.test_client()
        self.client.testing = True

    def test_invalid_url_page_not_found(self):
        result = self.client.get('/page/not/found')
        self.assertEqual(result.status_code, 404)

    def test_invalid_mulungwishi_query(self):
        result = self.client.get('/query?no_content')
        self.assertEqual(result.status_code, 400)

    def test_invalid_mulungwishi_query_empty(self):
        result = self.client.get('/query?content&from&to')
        self.assertEqual(result.status_code, 400)

    def test_invalid_mulungwishi_query_no_value_assigned(self):
        result = self.client.get('/query?content=&from=&to=')
        self.assertEqual(result.status_code, 400)

    def test_invalid_mulungwishi_query_none(self):
        result = self.client.get('/query?')
        self.assertEqual(result.status_code, 400)

    def test_invalid_mulungwishi_query_empty_num_from(self):
        invalid_query_empty_num_from = "content=farmer_sms&from&to=number+to"
        result = self.client.get('/query?{}'.format(invalid_query_empty_num_from))
        self.assertEqual(result.status_code, 400)

    def test_invalid_mulungwishi_query_empty_num_to(self):
        invalid_query_empty_num_to = "content=farmer_sms&from=number+from&to"
        result = self.client.get('/query?{}'.format(invalid_query_empty_num_to))
        self.assertEqual(result.status_code, 400)

    def test_valid_mulungwishi_url(self):
        result = self.client.get('/')
        self.assertEqual(result.status_code, 200)

    def test_valid_mulungwishi_query(self):
        valid_query = "content=farmer_sms&from=engagespark+platform&to=mulungwishi_app"
        result = self.client.get('/query?{}'.format(valid_query))
        self.assertEqual(result.status_code, 200)

    def test_invalid_weather_url_none(self):
        result = self.client.get('/weather_forecast?')
        self.assertEqual(result.status_code, 400)

    def test_invalid_weather_url_no_value_assigned(self):
        result = self.client.get('/weather_forecast?address')
        self.assertEqual(result.status_code, 400)

    def test_invalid_weather_url_empty(self):
        result = self.client.get('/weather_forecast?address=')
        self.assertEqual(result.status_code, 400)

    @patch('app.weather_parser.WeatherForecast.check_forecast_api_is_present')
    @patch('app.geolocation_api_parser.Geolocation.check_geolocation_api_keys_are_present')
    @patch('app.geolocation_api_parser.Geolocation.is_place_query_valid')
    def test_invalid_weather_url_invalid_address(
        self,
        is_place_query_valid,
        check_geolocation_api_keys_are_present,
        check_forecast_api_is_present
    ):
        is_place_query_valid.return_value = False
        check_geolocation_api_keys_are_present.return_value = True
        check_forecast_api_is_present = True
        result = self.client.get('/weather_forecast?address=pppppppppp')
        self.assertTrue(is_place_query_valid.called)
        self.assertEqual(result.status_code, 400)

    @patch('app.weather_parser.WeatherForecast.check_forecast_api_is_present')
    @patch('app.weather_parser.WeatherForecast.generate_forecast')
    @patch('app.geolocation_api_parser.Geolocation.check_geolocation_api_keys_are_present')
    @patch('app.geolocation_api_parser.Geolocation.local_time')
    @patch('app.geolocation_api_parser.Geolocation.get_address_query')
    def test_valid_weather_url_valid_address(
        self,
        get_address_query,
        local_time,
        check_geolocation_api_keys_are_present,
        generate_forecast,
        check_forecast_api_is_present
    ):
        get_address_query.return_value = {
        'results': [{
            'geometry': {
                'location': {
                    'lat': 10.3338299, 'lng': 123.8941434
                }
            }
        }], 
        'status': 'OK'
        }
        local_time = '2013-05-06T12:00:00'
        check_geolocation_api_keys_are_present.return_value = True
        mock_currently = {
        'currently': {
            'summary': 'Partly Cloudy',
            'temperature': 31.79,
            'time': 1460439452,
            'precipProbability': 0.02,
            'humidity': 0.58,
            }
        }
        check_geolocation_api_keys_are_present.return_value = True
        generate_forecast.return_value = mock_currently
        result = self.client.get('/weather_forecast?address=Lahug, Cebu City')
        self.assertTrue(generate_forecast.called)
        self.assertTrue(get_address_query.called)
        self.assertEqual(result.status_code, 200)
        self.assertTrue('Temp: -0.12C / 31.79F' in str(result.data))
        self.assertTrue('Humidity: 57%' in str(result.data))
        self.assertTrue('Precip: 2%' in str(result.data))
        self.assertTrue('Summary: Partly Cloudy' in str(result.data))
