import forecastio
from config import FORECAST_API_KEY


class WeatherForecast:

    def generate_forecast(self, latitude, longitude):
        forecast = self.get_forecast_request(latitude, longitude)
        return forecast.currently()

    def get_forecast_request(self, latitude, longitude):
        return forecastio.load_forecast(FORECAST_API_KEY, latitude, longitude)
