import datetime
import pandas as pd

from src.weather.client import WeatherClient
from src.weather.schemas import WeatherRequest, WeatherResponse, HourlyWeatherData
from src.core.exceptions.weather import WeatherForecastExceedsMaxFutureDate, WeatherForecastAPILimitExceeded


class WeatherService:
    def __init__(self, weather_client: WeatherClient):
        self.weather_client = weather_client

    def get_weather(self, request: WeatherRequest) -> WeatherResponse:
        current_date = datetime.date.today()
        historical_data_cutoff = current_date - datetime.timedelta(days=5)

        if not self._is_data_within_16_days(current_date, request.end_date) or not self._is_data_within_16_days(
                current_date, request.start_date):
            raise WeatherForecastExceedsMaxFutureDate()

        # check the date range of the request, to understand if we need to fetch historical data, forecast data or both
        # fetch historical data
        if request.end_date < historical_data_cutoff:
            hourly_weather_data = self._get_hourly_history_weather(request.latitude, request.longitude, request.start_date,
                                                                   request.end_date, request.azimuth, request.tilt)
            weather_data = WeatherResponse(latitude=request.latitude, longitude=request.longitude, start_date=request.start_date,
                                           end_date=request.end_date, hourly=hourly_weather_data)
            return weather_data
        # fetch forecast data
        elif request.start_date >= historical_data_cutoff:
            hourly_weather_data = self._get_hourly_forecast_weather(request.latitude, request.longitude, request.start_date,
                                                                    request.end_date, request.azimuth, request.tilt)
            weather_data = WeatherResponse(latitude=request.latitude, longitude=request.longitude, start_date=request.start_date,
                                           end_date=request.end_date, hourly=hourly_weather_data)
            return weather_data
        # fetch historical and forecast data
        else:
            historical_weather_data = self._get_hourly_history_weather(request.latitude, request.longitude, request.start_date,
                                                                       historical_data_cutoff, request.azimuth, request.tilt)
            forecast_weather_data = self._get_hourly_forecast_weather(request.latitude, request.longitude, historical_data_cutoff,
                                                                      request.end_date, request.azimuth, request.tilt)

            response = WeatherResponse(
                latitude=request.latitude,
                longitude=request.longitude,
                start_date=request.start_date,
                end_date=request.end_date,
                hourly=historical_weather_data + forecast_weather_data
            )
            return response

    def _get_hourly_history_weather(self, latitude, longitude, start_date, end_date, azimuth, tilt) -> list[
        HourlyWeatherData]:
        historical_weather_data = self.weather_client.fetch_historical_weather(
            latitude=latitude,
            longitude=longitude,
            start_date=start_date,
            end_date=end_date,
            azimuth=azimuth,
            tilt=tilt,
        )
        hourly_weather_data = pd.DataFrame(historical_weather_data["hourly"]).to_dict("records")
        historical_weather_data = [HourlyWeatherData(**data) for data in hourly_weather_data]

        return historical_weather_data

    def _get_hourly_forecast_weather(self, latitude, longitude, start_date, end_date, azimuth, tilt) -> list[
        HourlyWeatherData]:
        current_date = datetime.date.today()

        if not self._is_data_within_16_days(current_date, end_date) or not self._is_data_within_16_days(current_date, start_date):
            raise WeatherForecastExceedsMaxFutureDate()

        forecast_weather_data = self.weather_client.fetch_forecast_weather(
            latitude=latitude,
            longitude=longitude,
            azimuth=azimuth,
            tilt=tilt,
            start_date=start_date,
            end_date=end_date
        )
        hourly_weather_data = pd.DataFrame(forecast_weather_data["hourly"]).to_dict("records")
        forecast_weather_data = [HourlyWeatherData(**data) for data in hourly_weather_data]

        return forecast_weather_data

    def _is_data_within_16_days(self, today_date, date_to_verify):
        max_allowed_date = today_date + datetime.timedelta(days=16)
        return date_to_verify <= max_allowed_date
