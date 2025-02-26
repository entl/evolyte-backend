import pandas as pd

from src.weather.client import WeatherClient
from src.weather.schemas import WeatherRequest, WeatherResponse, HourlyWeatherData


class WeatherService:
    def __init__(self, weather_client: WeatherClient):
        self.weather_client = weather_client

    def get_weather_data(self, request: WeatherRequest) -> WeatherResponse:
        weather_data = self.weather_client.fetch_weather_data(**request.model_dump())
        hourly_weather_data = pd.DataFrame(weather_data.get("hourly", []))
        hourly_weather_data = hourly_weather_data.to_dict(orient="records")

        hourly_weather_schema = [HourlyWeatherData(**data) for data in hourly_weather_data]
        response = WeatherResponse(latitude=request.latitude, longitude=request.longitude,
                                   start_date=request.start_date, end_date=request.end_date,
                                   hourly=hourly_weather_schema)

        return response
