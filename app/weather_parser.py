import forecastio
from config import FORECAST_API_KEY


class WeatherForecast:

    def generate_forecast(self, latitude, longitude, frequency):
        forecast = self.get_forecast_request(latitude, longitude)
        if frequency == 'hourly':
            return forecast.hourly()
        elif frequency == 'daily':
            return forecast.daily()
        return forecast.currently()

    def get_forecast_request(self, latitude, longitude):
        return forecastio.load_forecast(FORECAST_API_KEY, latitude, longitude)
