#!/usr/bin/env python
import forecastio
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

    @patch('app.geocode_api_parser.Geocode.is_place_query_valid')
    def test_invalid_weather_url_invalid_address(self, is_place_query_valid,):
        is_place_query_valid.return_value = False
        result = self.client.get('/weather_forecast?address=pppppppppp')
        self.assertTrue(is_place_query_valid.called)
        self.assertEqual(result.status_code, 400)

    @patch('app.weather_parser.WeatherForecast.generate_forecast')
    @patch('app.geocode_api_parser.Geocode.get_coordinates')
    @patch('app.geocode_api_parser.Geocode.get_place_info')
    @patch('app.geocode_api_parser.Geocode.is_place_query_valid')
    def test_valid_weather_url_valid_address(self, is_place_query_valid, get_place_info, get_coordinates, generate_forecast):
        is_place_query_valid.return_value = True
        get_coordinates.return_value = {'lat': 10.3338299, 'lng': 123.8941434}
        get_place_info.return_value = {
            'formatted_address': 'Lahug, Cebu City, Cebu, Philippines',
            'place_type': 'neighborhood'
        }
        mock_currently = {'precipIntensity': 0.0305, 'ozone': 241.16, 'windBearing': 76, 'icon': 'partly-cloudy-day', 'summary': 'Partly Cloudy', 'apparentTemperature': 36.11, 'temperature': 31.79, 'time': 1460439452, 'pressure': 1008.13, 'precipProbability': 0.02, 'humidity': 0.58, 'cloudCover': 0.55, 'precipType': 'rain', 'windSpeed': 3.25, 'dewPoint': 22.58}
        generate_forecast.return_value = forecastio.models.ForecastioDataPoint(d=mock_currently)

        result = self.client.get('/weather_forecast?address=Lahug, Cebu City')
        self.assertTrue(is_place_query_valid.called)
        self.assertTrue(generate_forecast.called)
        self.assertTrue(get_place_info.called)
        self.assertEqual(result.status_code, 200)
        self.assertTrue('Temperature: 31.79' in str(result.data))
        self.assertTrue('Humidity: 0.58' in str(result.data))
        self.assertTrue('Probability of Precipitation: 0.02' in str(result.data))
        self.assertTrue('Weather Summary: Partly Cloudy' in str(result.data))

    @patch('app.weather_parser.WeatherForecast.generate_forecast')
    @patch('app.geocode_api_parser.Geocode.get_coordinates')
    @patch('app.geocode_api_parser.Geocode.get_place_info')
    @patch('app.geocode_api_parser.Geocode.is_place_query_valid')
    def test_valid_weather_url_valid_address_currently(self, is_place_query_valid, get_place_info, get_coordinates, generate_forecast):
        is_place_query_valid.return_value = True
        get_coordinates.return_value = {'lat': 10.3338299, 'lng': 123.8941434}
        get_place_info.return_value = {
            'formatted_address': 'Lahug, Cebu City, Cebu, Philippines',
            'place_type': 'neighborhood'
        }
        mock_currently = {'precipIntensity': 0.0305, 'ozone': 241.16, 'windBearing': 76, 'icon': 'partly-cloudy-day', 'summary': 'Partly Cloudy', 'apparentTemperature': 36.11, 'temperature': 31.79, 'time': 1460439452, 'pressure': 1008.13, 'precipProbability': 0.02, 'humidity': 0.58, 'cloudCover': 0.55, 'precipType': 'rain', 'windSpeed': 3.25, 'dewPoint': 22.58}
        generate_forecast.return_value = forecastio.models.ForecastioDataPoint(d=mock_currently)

        result = self.client.get('/weather_forecast?address=Lahug, Cebu City')
        self.assertTrue(is_place_query_valid.called)
        self.assertTrue(generate_forecast.called)
        self.assertTrue(get_place_info.called)
        self.assertEqual(result.status_code, 200)
        self.assertTrue('Temperature: 31.79' in str(result.data))
        self.assertTrue('Humidity: 0.58' in str(result.data))
        self.assertTrue('Probability of Precipitation: 0.02' in str(result.data))
        self.assertTrue('Weather Summary: Partly Cloudy' in str(result.data))

    @patch('app.weather_parser.WeatherForecast.generate_forecast')
    @patch('app.geocode_api_parser.Geocode.get_coordinates')
    @patch('app.geocode_api_parser.Geocode.get_place_info')
    @patch('app.geocode_api_parser.Geocode.is_place_query_valid')
    def test_valid_weather_url_valid_address_hourly(self, is_place_query_valid, get_place_info, get_coordinates, generate_forecast):
        is_place_query_valid.return_value = True
        get_coordinates.return_value = {'lat': 10.3338299, 'lng': 123.8941434}
        get_place_info.return_value = {'formatted_address': 'Lahug, Cebu City, Cebu, Philippines', 'place_type': 'neighborhood'}
        mock_hourly = {
            "summary": "Light rain starting this evening, continuing until tomorrow morning.",
            "icon": "rain",
            "data": [
                {
                    "time": 1460440800,
                    "summary": "Partly Cloudy",
                    "icon": "partly-cloudy-day",
                    "precipIntensity": 0.0031,
                    "precipProbability": 0.11,
                    "precipType": "rain",
                    "temperature": 89.06,
                    "apparentTemperature": 96.93,
                    "dewPoint": 72.79,
                    "humidity": 0.59,
                    "windSpeed": 7.16,
                    "windBearing": 75,
                    "cloudCover": 0.53,
                    "pressure": 1007.94,
                    "ozone": 241.16
                }
            ]
        }
        generate_forecast.return_value = forecastio.models.ForecastioDataBlock(d=mock_hourly)
        result = self.client.get('/weather_forecast?address=Lahug, Cebu City hourly')
        self.assertTrue(is_place_query_valid.called)
        self.assertTrue(generate_forecast.called)
        self.assertTrue(get_place_info.called)
        self.assertEqual(result.status_code, 200)
        self.assertTrue('temperature: 89.06' in str(result.data))
        self.assertTrue('humidity: 0.59' in str(result.data))
        self.assertTrue('precipProbability: 0.11' in str(result.data))
        self.assertTrue('summary: Partly Cloudy' in str(result.data))

    @patch('app.weather_parser.WeatherForecast.generate_forecast')
    @patch('app.geocode_api_parser.Geocode.get_coordinates')
    @patch('app.geocode_api_parser.Geocode.get_place_info')
    @patch('app.geocode_api_parser.Geocode.is_place_query_valid')
    def test_valid_weather_url_valid_address_daily(self, is_place_query_valid, get_place_info, get_coordinates, generate_forecast):
        is_place_query_valid.return_value = True
        get_place_info.return_value = {'formatted_address': 'Lahug, Cebu City, Cebu, Philippines', 'place_type': 'neighborhood'}
        get_coordinates.return_value = {'lat': 10.3338299, 'lng': 123.8941434}
        mock_daily = {
            "summary": "Light rain throughout the week, with temperatures falling to 90°F on Wednesday.",
            "icon": "rain",
            "data": [
                {
                    "time": 1460476800,
                    "summary": "Light rain in the morning and evening.",
                    "icon": "rain",
                    "sunriseTime": 1460496959,
                    "sunsetTime": 1460541369,
                    "moonPhase": 0.21,
                    "precipIntensity": 0.0062,
                    "precipIntensityMax": 0.0158,
                    "precipIntensityMaxTime": 1460484000,
                    "precipProbability": 0.56,
                    "precipType": "rain",
                    "temperatureMin": 79.33,
                    "temperatureMinTime": 1460491200,
                    "temperatureMax": 92.18,
                    "temperatureMaxTime": 1460527200,
                    "apparentTemperatureMin": 79.82,
                    "apparentTemperatureMinTime": 1460491200,
                    "apparentTemperatureMax": 105.69,
                    "apparentTemperatureMaxTime": 1460527200,
                    "dewPoint": 75.28,
                    "humidity": 0.75,
                    "windSpeed": 6.56,
                    "windBearing": 85,
                    "cloudCover": 0.7,
                    "pressure": 1009.38,
                    "ozone": 241.73
                }
            ]
        }
        generate_forecast.return_value = forecastio.models.ForecastioDataBlock(d=mock_daily)
        result = self.client.get('/weather_forecast?address=Lahug, Cebu City daily')
        self.assertTrue(is_place_query_valid.called)
        self.assertTrue(generate_forecast.called)
        self.assertTrue(get_place_info.called)
        self.assertEqual(result.status_code, 200)
        self.assertTrue('temperatureMin: 79.33' in str(result.data))
        self.assertTrue('temperatureMax: 92.18' in str(result.data))
        self.assertTrue('humidity: 0.75' in str(result.data))
        self.assertTrue('precipProbability: 0.56' in str(result.data))
        self.assertTrue('summary: Light rain in the morning and evening.' in str(result.data))
