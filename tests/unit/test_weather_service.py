import datetime
from unittest.mock import MagicMock, Mock, patch
import pytest
import pandas as pd

from src.core.exceptions.weather import (
    WeatherForecastAPILimitExceeded,
    WeatherForecastExceedsMaxFutureDate,
)
from src.weather.client import WeatherClient
from src.weather.schemas import HourlyWeatherData, WeatherRequest, WeatherResponse
from src.weather.service import WeatherService  # Adjust import path as needed


class TestWeatherService:
    @pytest.fixture
    def mock_weather_client(self):
        """Mock weather client fixture"""
        return MagicMock(spec=WeatherClient)

    @pytest.fixture
    def mock_clock(self):
        """Mock clock fixture that returns a fixed date"""
        return MagicMock(return_value=datetime.date(2024, 6, 15))

    @pytest.fixture
    def weather_service(self, mock_weather_client, mock_clock):
        """Weather service fixture with mocked dependencies"""
        return WeatherService(
            weather_client=mock_weather_client, clock=mock_clock, historical_days_cutoff=5, max_forecast_days=16
        )

    @pytest.fixture
    def sample_weather_request(self):
        """Sample weather request fixture"""
        return WeatherRequest(
            latitude=40.7128,
            longitude=-74.0060,
            start_date=datetime.date(2024, 6, 10),
            end_date=datetime.date(2024, 6, 12),
            azimuth=180,
            tilt=30,
        )

    @pytest.fixture
    def sample_hourly_data(self):
        """Sample hourly weather data fixture"""
        return {
            "hourly": [
                {
                    "time": "2024-01-01T00:00",
                    "temperature_2m": 8.2,
                    "apparent_temperature": 2.4,
                    "relative_humidity_2m": 74.0,
                    "dew_point_2m": 3.8,
                    "pressure_msl": 994.8,
                    "surface_pressure": 994.1,
                    "precipitation": 0.0,
                    "cloud_cover": 95.0,
                    "et0_fao_evapotranspiration": 0.05,
                    "wind_speed_10m": 29.3,
                    "wind_direction_10m": 249.0,
                    "shortwave_radiation": 0.0,
                    "diffuse_radiation": 0.0,
                    "direct_radiation": 0.0,
                    "direct_normal_irradiance": 0.0,
                    "terrestrial_radiation": 0.0,
                    "is_day": 0,
                    "sunshine_duration": 0.0,
                    "weather_code": 3,
                },
                {
                    "time": "2024-01-01T01:00",
                    "temperature_2m": 7.8,
                    "apparent_temperature": 2.0,
                    "relative_humidity_2m": 76.0,
                    "dew_point_2m": 3.7,
                    "pressure_msl": 995.8,
                    "surface_pressure": 995.1,
                    "precipitation": 0.0,
                    "cloud_cover": 5.0,
                    "et0_fao_evapotranspiration": 0.04,
                    "wind_speed_10m": 29.7,
                    "wind_direction_10m": 247.0,
                    "shortwave_radiation": 0.0,
                    "diffuse_radiation": 0.0,
                    "direct_radiation": 0.0,
                    "direct_normal_irradiance": 0.0,
                    "terrestrial_radiation": 0.0,
                    "is_day": 0,
                    "sunshine_duration": 0.0,
                    "weather_code": 0,
                },
                {
                    "time": "2024-01-01T02:00",
                    "temperature_2m": 7.3,
                    "apparent_temperature": 1.7,
                    "relative_humidity_2m": 79.0,
                    "dew_point_2m": 3.9,
                    "pressure_msl": 996.8,
                    "surface_pressure": 996.1,
                    "precipitation": 0.0,
                    "cloud_cover": 17.0,
                    "et0_fao_evapotranspiration": 0.03,
                    "wind_speed_10m": 28.6,
                    "wind_direction_10m": 251.0,
                    "shortwave_radiation": 0.0,
                    "diffuse_radiation": 0.0,
                    "direct_radiation": 0.0,
                    "direct_normal_irradiance": 0.0,
                    "terrestrial_radiation": 0.0,
                    "is_day": 0,
                    "sunshine_duration": 0.0,
                    "weather_code": 0,
                },
                {
                    "time": "2024-01-01T03:00",
                    "temperature_2m": 7.2,
                    "apparent_temperature": 1.9,
                    "relative_humidity_2m": 80.0,
                    "dew_point_2m": 3.9,
                    "pressure_msl": 997.7,
                    "surface_pressure": 997.0,
                    "precipitation": 0.0,
                    "cloud_cover": 29.0,
                    "et0_fao_evapotranspiration": 0.03,
                    "wind_speed_10m": 26.8,
                    "wind_direction_10m": 253.0,
                    "shortwave_radiation": 0.0,
                    "diffuse_radiation": 0.0,
                    "direct_radiation": 0.0,
                    "direct_normal_irradiance": 0.0,
                    "terrestrial_radiation": 0.0,
                    "is_day": 0,
                    "sunshine_duration": 0.0,
                    "weather_code": 1,
                },
                {
                    "time": "2024-01-01T04:00",
                    "temperature_2m": 7.1,
                    "apparent_temperature": 1.6,
                    "relative_humidity_2m": 79.0,
                    "dew_point_2m": 3.7,
                    "pressure_msl": 998.7,
                    "surface_pressure": 998.0,
                    "precipitation": 0.0,
                    "cloud_cover": 4.0,
                    "et0_fao_evapotranspiration": 0.03,
                    "wind_speed_10m": 27.1,
                    "wind_direction_10m": 253.0,
                    "shortwave_radiation": 0.0,
                    "diffuse_radiation": 0.0,
                    "direct_radiation": 0.0,
                    "direct_normal_irradiance": 0.0,
                    "terrestrial_radiation": 0.0,
                    "is_day": 0,
                    "sunshine_duration": 0.0,
                    "weather_code": 0,
                },
                {
                    "time": "2024-01-01T05:00",
                    "temperature_2m": 7.1,
                    "apparent_temperature": 1.6,
                    "relative_humidity_2m": 76.0,
                    "dew_point_2m": 3.2,
                    "pressure_msl": 999.5,
                    "surface_pressure": 998.8,
                    "precipitation": 0.0,
                    "cloud_cover": 4.0,
                    "et0_fao_evapotranspiration": 0.04,
                    "wind_speed_10m": 26.9,
                    "wind_direction_10m": 258.0,
                    "shortwave_radiation": 0.0,
                    "diffuse_radiation": 0.0,
                    "direct_radiation": 0.0,
                    "direct_normal_irradiance": 0.0,
                    "terrestrial_radiation": 0.0,
                    "is_day": 0,
                    "sunshine_duration": 0.0,
                    "weather_code": 0,
                },
                {
                    "time": "2024-01-01T06:00",
                    "temperature_2m": 6.8,
                    "apparent_temperature": 1.4,
                    "relative_humidity_2m": 74.0,
                    "dew_point_2m": 2.5,
                    "pressure_msl": 1000.4,
                    "surface_pressure": 999.7,
                    "precipitation": 0.0,
                    "cloud_cover": 49.0,
                    "et0_fao_evapotranspiration": 0.04,
                    "wind_speed_10m": 25.1,
                    "wind_direction_10m": 257.0,
                    "shortwave_radiation": 0.0,
                    "diffuse_radiation": 0.0,
                    "direct_radiation": 0.0,
                    "direct_normal_irradiance": 0.0,
                    "terrestrial_radiation": 0.0,
                    "is_day": 0,
                    "sunshine_duration": 0.0,
                    "weather_code": 1,
                },
                {
                    "time": "2024-01-01T07:00",
                    "temperature_2m": 6.5,
                    "apparent_temperature": 1.3,
                    "relative_humidity_2m": 72.0,
                    "dew_point_2m": 1.9,
                    "pressure_msl": 1001.6,
                    "surface_pressure": 1000.9,
                    "precipitation": 0.0,
                    "cloud_cover": 99.0,
                    "et0_fao_evapotranspiration": 0.04,
                    "wind_speed_10m": 23.6,
                    "wind_direction_10m": 258.0,
                    "shortwave_radiation": 0.0,
                    "diffuse_radiation": 0.0,
                    "direct_radiation": 0.0,
                    "direct_normal_irradiance": 0.0,
                    "terrestrial_radiation": 0.0,
                    "is_day": 0,
                    "sunshine_duration": 0.0,
                    "weather_code": 3,
                },
                {
                    "time": "2024-01-01T08:00",
                    "temperature_2m": 6.2,
                    "apparent_temperature": 1.4,
                    "relative_humidity_2m": 71.0,
                    "dew_point_2m": 1.4,
                    "pressure_msl": 1002.7,
                    "surface_pressure": 1002.0,
                    "precipitation": 0.0,
                    "cloud_cover": 99.0,
                    "et0_fao_evapotranspiration": 0.03,
                    "wind_speed_10m": 19.6,
                    "wind_direction_10m": 256.0,
                    "shortwave_radiation": 0.0,
                    "diffuse_radiation": 0.0,
                    "direct_radiation": 0.0,
                    "direct_normal_irradiance": 0.0,
                    "terrestrial_radiation": 0.0,
                    "is_day": 0,
                    "sunshine_duration": 0.0,
                    "weather_code": 3,
                },
                {
                    "time": "2024-01-01T09:00",
                    "temperature_2m": 6.5,
                    "apparent_temperature": 1.8,
                    "relative_humidity_2m": 69.0,
                    "dew_point_2m": 1.3,
                    "pressure_msl": 1003.5,
                    "surface_pressure": 1002.8,
                    "precipitation": 0.0,
                    "cloud_cover": 100.0,
                    "et0_fao_evapotranspiration": 0.05,
                    "wind_speed_10m": 18.9,
                    "wind_direction_10m": 256.0,
                    "shortwave_radiation": 17.0,
                    "diffuse_radiation": 15.0,
                    "direct_radiation": 2.0,
                    "direct_normal_irradiance": 23.9,
                    "terrestrial_radiation": 59.0,
                    "is_day": 1,
                    "sunshine_duration": 0.0,
                    "weather_code": 3,
                },
                {
                    "time": "2024-01-01T10:00",
                    "temperature_2m": 7.1,
                    "apparent_temperature": 2.6,
                    "relative_humidity_2m": 69.0,
                    "dew_point_2m": 1.8,
                    "pressure_msl": 1004.0,
                    "surface_pressure": 1003.3,
                    "precipitation": 0.0,
                    "cloud_cover": 98.0,
                    "et0_fao_evapotranspiration": 0.06,
                    "wind_speed_10m": 18.5,
                    "wind_direction_10m": 249.0,
                    "shortwave_radiation": 68.0,
                    "diffuse_radiation": 62.0,
                    "direct_radiation": 6.0,
                    "direct_normal_irradiance": 41.8,
                    "terrestrial_radiation": 202.9,
                    "is_day": 1,
                    "sunshine_duration": 0.0,
                    "weather_code": 3,
                },
                {
                    "time": "2024-01-01T11:00",
                    "temperature_2m": 8.0,
                    "apparent_temperature": 3.7,
                    "relative_humidity_2m": 68.0,
                    "dew_point_2m": 2.4,
                    "pressure_msl": 1004.3,
                    "surface_pressure": 1003.6,
                    "precipitation": 0.0,
                    "cloud_cover": 99.0,
                    "et0_fao_evapotranspiration": 0.08,
                    "wind_speed_10m": 17.6,
                    "wind_direction_10m": 244.0,
                    "shortwave_radiation": 134.0,
                    "diffuse_radiation": 99.0,
                    "direct_radiation": 35.0,
                    "direct_normal_irradiance": 159.4,
                    "terrestrial_radiation": 310.5,
                    "is_day": 1,
                    "sunshine_duration": 2983.32,
                    "weather_code": 3,
                },
                {
                    "time": "2024-01-01T12:00",
                    "temperature_2m": 8.4,
                    "apparent_temperature": 4.9,
                    "relative_humidity_2m": 70.0,
                    "dew_point_2m": 3.2,
                    "pressure_msl": 1004.4,
                    "surface_pressure": 1003.7,
                    "precipitation": 0.0,
                    "cloud_cover": 95.0,
                    "et0_fao_evapotranspiration": 0.08,
                    "wind_speed_10m": 13.3,
                    "wind_direction_10m": 229.0,
                    "shortwave_radiation": 157.0,
                    "diffuse_radiation": 120.0,
                    "direct_radiation": 37.0,
                    "direct_normal_irradiance": 142.4,
                    "terrestrial_radiation": 367.5,
                    "is_day": 1,
                    "sunshine_duration": 2472.54,
                    "weather_code": 3,
                },
                {
                    "time": "2024-01-01T13:00",
                    "temperature_2m": 8.6,
                    "apparent_temperature": 5.2,
                    "relative_humidity_2m": 74.0,
                    "dew_point_2m": 4.2,
                    "pressure_msl": 1004.6,
                    "surface_pressure": 1003.9,
                    "precipitation": 0.0,
                    "cloud_cover": 100.0,
                    "et0_fao_evapotranspiration": 0.08,
                    "wind_speed_10m": 13.8,
                    "wind_direction_10m": 221.0,
                    "shortwave_radiation": 142.0,
                    "diffuse_radiation": 118.0,
                    "direct_radiation": 24.0,
                    "direct_normal_irradiance": 91.8,
                    "terrestrial_radiation": 370.0,
                    "is_day": 1,
                    "sunshine_duration": 952.68,
                    "weather_code": 3,
                },
                {
                    "time": "2024-01-01T14:00",
                    "temperature_2m": 8.8,
                    "apparent_temperature": 5.7,
                    "relative_humidity_2m": 77.0,
                    "dew_point_2m": 5.0,
                    "pressure_msl": 1003.8,
                    "surface_pressure": 1003.1,
                    "precipitation": 0.0,
                    "cloud_cover": 100.0,
                    "et0_fao_evapotranspiration": 0.06,
                    "wind_speed_10m": 12.2,
                    "wind_direction_10m": 204.0,
                    "shortwave_radiation": 124.0,
                    "diffuse_radiation": 100.0,
                    "direct_radiation": 24.0,
                    "direct_normal_irradiance": 106.8,
                    "terrestrial_radiation": 317.8,
                    "is_day": 1,
                    "sunshine_duration": 1404.46,
                    "weather_code": 3,
                },
                {
                    "time": "2024-01-01T15:00",
                    "temperature_2m": 8.6,
                    "apparent_temperature": 5.4,
                    "relative_humidity_2m": 80.0,
                    "dew_point_2m": 5.3,
                    "pressure_msl": 1003.4,
                    "surface_pressure": 1002.7,
                    "precipitation": 0.0,
                    "cloud_cover": 100.0,
                    "et0_fao_evapotranspiration": 0.04,
                    "wind_speed_10m": 13.8,
                    "wind_direction_10m": 200.0,
                    "shortwave_radiation": 58.0,
                    "diffuse_radiation": 52.0,
                    "direct_radiation": 6.0,
                    "direct_normal_irradiance": 39.6,
                    "terrestrial_radiation": 214.6,
                    "is_day": 1,
                    "sunshine_duration": 0.0,
                    "weather_code": 3,
                },
                {
                    "time": "2024-01-01T16:00",
                    "temperature_2m": 8.2,
                    "apparent_temperature": 4.8,
                    "relative_humidity_2m": 81.0,
                    "dew_point_2m": 5.2,
                    "pressure_msl": 1002.6,
                    "surface_pressure": 1001.9,
                    "precipitation": 0.1,
                    "cloud_cover": 100.0,
                    "et0_fao_evapotranspiration": 0.03,
                    "wind_speed_10m": 15.5,
                    "wind_direction_10m": 192.0,
                    "shortwave_radiation": 9.0,
                    "diffuse_radiation": 9.0,
                    "direct_radiation": 0.0,
                    "direct_normal_irradiance": 0.0,
                    "terrestrial_radiation": 67.2,
                    "is_day": 1,
                    "sunshine_duration": 0.0,
                    "weather_code": 51,
                },
                {
                    "time": "2024-01-01T17:00",
                    "temperature_2m": 8.2,
                    "apparent_temperature": 4.8,
                    "relative_humidity_2m": 85.0,
                    "dew_point_2m": 5.7,
                    "pressure_msl": 1001.6,
                    "surface_pressure": 1000.9,
                    "precipitation": 0.4,
                    "cloud_cover": 100.0,
                    "et0_fao_evapotranspiration": 0.01,
                    "wind_speed_10m": 15.9,
                    "wind_direction_10m": 174.0,
                    "shortwave_radiation": 0.0,
                    "diffuse_radiation": 0.0,
                    "direct_radiation": 0.0,
                    "direct_normal_irradiance": 0.0,
                    "terrestrial_radiation": 0.0,
                    "is_day": 0,
                    "sunshine_duration": 0.0,
                    "weather_code": 51,
                },
                {
                    "time": "2024-01-01T18:00",
                    "temperature_2m": 8.5,
                    "apparent_temperature": 4.7,
                    "relative_humidity_2m": 90.0,
                    "dew_point_2m": 7.0,
                    "pressure_msl": 1000.2,
                    "surface_pressure": 999.5,
                    "precipitation": 0.6,
                    "cloud_cover": 100.0,
                    "et0_fao_evapotranspiration": 0.01,
                    "wind_speed_10m": 20.9,
                    "wind_direction_10m": 177.0,
                    "shortwave_radiation": 0.0,
                    "diffuse_radiation": 0.0,
                    "direct_radiation": 0.0,
                    "direct_normal_irradiance": 0.0,
                    "terrestrial_radiation": 0.0,
                    "is_day": 0,
                    "sunshine_duration": 0.0,
                    "weather_code": 53,
                },
                {
                    "time": "2024-01-01T19:00",
                    "temperature_2m": 8.9,
                    "apparent_temperature": 4.7,
                    "relative_humidity_2m": 90.0,
                    "dew_point_2m": 7.4,
                    "pressure_msl": 998.3,
                    "surface_pressure": 997.6,
                    "precipitation": 0.8,
                    "cloud_cover": 100.0,
                    "et0_fao_evapotranspiration": 0.01,
                    "wind_speed_10m": 24.5,
                    "wind_direction_10m": 177.0,
                    "shortwave_radiation": 0.0,
                    "diffuse_radiation": 0.0,
                    "direct_radiation": 0.0,
                    "direct_normal_irradiance": 0.0,
                    "terrestrial_radiation": 0.0,
                    "is_day": 0,
                    "sunshine_duration": 0.0,
                    "weather_code": 53,
                },
                {
                    "time": "2024-01-01T20:00",
                    "temperature_2m": 9.3,
                    "apparent_temperature": 4.9,
                    "relative_humidity_2m": 90.0,
                    "dew_point_2m": 7.8,
                    "pressure_msl": 996.4,
                    "surface_pressure": 995.7,
                    "precipitation": 1.6,
                    "cloud_cover": 100.0,
                    "et0_fao_evapotranspiration": 0.01,
                    "wind_speed_10m": 25.7,
                    "wind_direction_10m": 174.0,
                    "shortwave_radiation": 0.0,
                    "diffuse_radiation": 0.0,
                    "direct_radiation": 0.0,
                    "direct_normal_irradiance": 0.0,
                    "terrestrial_radiation": 0.0,
                    "is_day": 0,
                    "sunshine_duration": 0.0,
                    "weather_code": 61,
                },
                {
                    "time": "2024-01-01T21:00",
                    "temperature_2m": 9.6,
                    "apparent_temperature": 5.1,
                    "relative_humidity_2m": 90.0,
                    "dew_point_2m": 8.1,
                    "pressure_msl": 994.0,
                    "surface_pressure": 993.3,
                    "precipitation": 2.2,
                    "cloud_cover": 100.0,
                    "et0_fao_evapotranspiration": 0.01,
                    "wind_speed_10m": 27.6,
                    "wind_direction_10m": 173.0,
                    "shortwave_radiation": 0.0,
                    "diffuse_radiation": 0.0,
                    "direct_radiation": 0.0,
                    "direct_normal_irradiance": 0.0,
                    "terrestrial_radiation": 0.0,
                    "is_day": 0,
                    "sunshine_duration": 0.0,
                    "weather_code": 61,
                },
                {
                    "time": "2024-01-01T22:00",
                    "temperature_2m": 10.1,
                    "apparent_temperature": 6.4,
                    "relative_humidity_2m": 90.0,
                    "dew_point_2m": 8.5,
                    "pressure_msl": 991.9,
                    "surface_pressure": 991.2,
                    "precipitation": 1.6,
                    "cloud_cover": 100.0,
                    "et0_fao_evapotranspiration": 0.01,
                    "wind_speed_10m": 22.8,
                    "wind_direction_10m": 185.0,
                    "shortwave_radiation": 0.0,
                    "diffuse_radiation": 0.0,
                    "direct_radiation": 0.0,
                    "direct_normal_irradiance": 0.0,
                    "terrestrial_radiation": 0.0,
                    "is_day": 0,
                    "sunshine_duration": 0.0,
                    "weather_code": 61,
                },
                {
                    "time": "2024-01-01T23:00",
                    "temperature_2m": 10.7,
                    "apparent_temperature": 6.3,
                    "relative_humidity_2m": 91.0,
                    "dew_point_2m": 9.3,
                    "pressure_msl": 989.3,
                    "surface_pressure": 988.6,
                    "precipitation": 2.0,
                    "cloud_cover": 100.0,
                    "et0_fao_evapotranspiration": 0.01,
                    "wind_speed_10m": 28.9,
                    "wind_direction_10m": 194.0,
                    "shortwave_radiation": 0.0,
                    "diffuse_radiation": 0.0,
                    "direct_radiation": 0.0,
                    "direct_normal_irradiance": 0.0,
                    "terrestrial_radiation": 0.0,
                    "is_day": 0,
                    "sunshine_duration": 0.0,
                    "weather_code": 61,
                },
            ]
        }

    def test_init_with_default_values(self, mock_weather_client):
        """Test initialization with default values"""
        service = WeatherService(mock_weather_client)

        assert service.weather_client == mock_weather_client
        assert service.historical_days_cutoff == 5
        assert service.max_forecast_days == 16
        assert service.clock == datetime.date.today

    def test_init_with_custom_values(self, mock_weather_client, mock_clock):
        """Test initialization with custom values"""
        service = WeatherService(
            weather_client=mock_weather_client, clock=mock_clock, historical_days_cutoff=3, max_forecast_days=10
        )

        assert service.weather_client == mock_weather_client
        assert service.clock == mock_clock
        assert service.historical_days_cutoff == 3
        assert service.max_forecast_days == 10

    def test_get_weather_historical_only(
        self, weather_service, sample_weather_request, sample_hourly_data, mock_weather_client
    ):
        """Test getting weather data for historical dates only"""
        # Set up dates that are all historical (before cutoff)
        sample_weather_request.start_date = datetime.date(2024, 6, 5)
        sample_weather_request.end_date = datetime.date(2024, 6, 8)

        mock_weather_client.fetch_historical_weather.return_value = sample_hourly_data

        with patch("pandas.DataFrame") as mock_df:
            mock_df.return_value.to_dict.return_value = sample_hourly_data["hourly"]

            result = weather_service.get_weather(sample_weather_request)

        # Verify historical weather was called
        mock_weather_client.fetch_historical_weather.assert_called_once_with(
            latitude=40.7128,
            longitude=-74.0060,
            start_date=datetime.date(2024, 6, 5),
            end_date=datetime.date(2024, 6, 8),
            azimuth=180,
            tilt=30,
        )

        # Verify forecast weather was not called
        mock_weather_client.fetch_forecast_weather.assert_not_called()

        # Verify response structure
        assert isinstance(result, WeatherResponse)
        assert result.latitude == 40.7128
        assert result.longitude == -74.0060
        assert result.start_date == datetime.date(2024, 6, 5)
        assert result.end_date == datetime.date(2024, 6, 8)

    def test_get_weather_forecast_only(
        self, weather_service, sample_weather_request, sample_hourly_data, mock_weather_client
    ):
        """Test getting weather data for forecast dates only"""
        # Set up dates that are all forecast (after cutoff)
        start_date = datetime.datetime.today().date() + datetime.timedelta(days=10)  # 10 days in the future
        end_date = datetime.datetime.today().date() + datetime.timedelta(days=15)  # 15 days in the future

        sample_weather_request.start_date = start_date
        sample_weather_request.end_date = end_date

        mock_weather_client.fetch_forecast_weather.return_value = sample_hourly_data

        with patch("pandas.DataFrame") as mock_df:
            mock_df.return_value.to_dict.return_value = sample_hourly_data["hourly"]

            result = weather_service.get_weather(sample_weather_request)

        # Verify forecast weather was called
        mock_weather_client.fetch_forecast_weather.assert_called_once_with(
            latitude=40.7128, longitude=-74.0060, azimuth=180, tilt=30, start_date=start_date, end_date=end_date
        )

        # Verify historical weather was not called
        mock_weather_client.fetch_historical_weather.assert_not_called()

        # Verify response structure
        assert isinstance(result, WeatherResponse)
        assert result.start_date == start_date
        assert result.end_date == end_date

    def test_get_weather_combined_historical_and_forecast(
        self, weather_service, sample_weather_request, sample_hourly_data, mock_weather_client
    ):
        """Test getting weather data that spans both historical and forecast periods"""
        # Set up dates that span both historical and forecast
        start_date = datetime.datetime.today().date() - datetime.timedelta(days=10)  # 10 days in the past
        end_date = datetime.date.today() + datetime.timedelta(days=5)  # 5 days in the future

        sample_weather_request.start_date = start_date
        sample_weather_request.end_date = end_date

        mock_weather_client.fetch_historical_weather.return_value = sample_hourly_data
        mock_weather_client.fetch_forecast_weather.return_value = sample_hourly_data

        with patch("pandas.DataFrame") as mock_df:
            mock_df.return_value.to_dict.return_value = sample_hourly_data["hourly"]

            result = weather_service.get_weather(sample_weather_request)

        # Verify both historical and forecast were called
        mock_weather_client.fetch_historical_weather.assert_called_once()
        mock_weather_client.fetch_forecast_weather.assert_called_once()

        # Check historical call arguments
        hist_call = mock_weather_client.fetch_historical_weather.call_args
        assert hist_call.kwargs["start_date"] == start_date

        # Check forecast call arguments
        forecast_call = mock_weather_client.fetch_forecast_weather.call_args
        assert forecast_call.kwargs["end_date"] == end_date

    def test_get_weather_exceeds_max_future_date_start(self, weather_service, sample_weather_request):
        """Test exception when start date exceeds maximum future date"""
        sample_weather_request.start_date = datetime.datetime.today().date() + datetime.timedelta(
            days=17
        )  # More than 16 days in the future
        sample_weather_request.end_date = datetime.datetime.today().date() + datetime.timedelta(
            days=20
        )  # Also more than 16 days

        with pytest.raises(WeatherForecastExceedsMaxFutureDate):
            weather_service.get_weather(sample_weather_request)

    def test_get_weather_exceeds_max_future_date_end(self, weather_service, sample_weather_request):
        """Test exception when end date exceeds maximum future date"""
        # Set end date beyond 16 days from current date (2024-06-15)
        sample_weather_request.start_date = datetime.datetime.today().date() + datetime.timedelta(
            days=17
        )  # More than 16 days in the future
        sample_weather_request.end_date = datetime.datetime.today().date() + datetime.timedelta(
            days=20
        )  # Also more than 16 days

        with pytest.raises(WeatherForecastExceedsMaxFutureDate):
            weather_service.get_weather(sample_weather_request)

    def test_get_hourly_history_weather(self, weather_service, sample_hourly_data, mock_weather_client):
        """Test _get_hourly_history_weather method"""
        mock_weather_client.fetch_historical_weather.return_value = sample_hourly_data

        with patch("pandas.DataFrame") as mock_df, patch("src.weather.schemas.HourlyWeatherData") as mock_hourly_data:
            mock_df.return_value.to_dict.return_value = sample_hourly_data["hourly"]
            mock_hourly_data.side_effect = lambda **kwargs: Mock(**kwargs)

            result = weather_service._get_hourly_history_weather(
                latitude=40.7128,
                longitude=-74.0060,
                start_date=datetime.date(2024, 6, 10),
                end_date=datetime.date(2024, 6, 12),
                azimuth=180,
                tilt=30,
            )

        # Verify client was called correctly
        mock_weather_client.fetch_historical_weather.assert_called_once_with(
            latitude=40.7128,
            longitude=-74.0060,
            start_date=datetime.date(2024, 6, 10),
            end_date=datetime.date(2024, 6, 12),
            azimuth=180,
            tilt=30,
        )

        # Verify data processing
        mock_df.assert_called_once_with(sample_hourly_data["hourly"])
        assert len(result) == 24  # Should match number of hourly data points

    def test_get_hourly_forecast_weather(self, weather_service, sample_hourly_data, mock_weather_client):
        """Test _get_hourly_forecast_weather method"""
        mock_weather_client.fetch_forecast_weather.return_value = sample_hourly_data

        start_date = datetime.datetime.today().date() + datetime.timedelta(days=5)  # 5 days in the future
        end_date = datetime.datetime.today().date() + datetime.timedelta(days=10)  # 10 days in the future

        with patch("pandas.DataFrame") as mock_df, patch("src.weather.schemas.HourlyWeatherData") as mock_hourly_data:
            mock_df.return_value.to_dict.return_value = sample_hourly_data["hourly"]
            mock_hourly_data.side_effect = lambda **kwargs: Mock(**kwargs)

            result = weather_service._get_hourly_forecast_weather(
                latitude=40.7128, longitude=-74.0060, start_date=start_date, end_date=end_date, azimuth=180, tilt=30
            )

        # Verify client was called correctly
        mock_weather_client.fetch_forecast_weather.assert_called_once_with(
            latitude=40.7128, longitude=-74.0060, azimuth=180, tilt=30, start_date=start_date, end_date=end_date
        )

        assert len(result) == 24

    def test_get_hourly_forecast_weather_exceeds_limit(self, weather_service):
        """Test _get_hourly_forecast_weather raises exception when dates exceed limit"""
        with pytest.raises(WeatherForecastExceedsMaxFutureDate):
            weather_service._get_hourly_forecast_weather(
                latitude=40.7128,
                longitude=-74.0060,
                start_date=datetime.datetime.today().date()
                + datetime.timedelta(days=17),  # More than 16 days in the future
                end_date=datetime.datetime.today().date() + datetime.timedelta(days=20),  # Also more than 16 days
                azimuth=180,
                tilt=30,
            )

    def test_is_data_within_16_days_true(self, weather_service):
        """Test _is_data_within_16_days returns True for valid dates"""
        today = datetime.date(2024, 6, 15)
        valid_date = datetime.date(2024, 6, 30)  # 15 days from today

        result = weather_service._is_data_within_16_days(today, valid_date)
        assert result is True

    def test_is_data_within_16_days_false(self, weather_service):
        """Test _is_data_within_16_days returns False for invalid dates"""
        today = datetime.date(2024, 6, 15)
        invalid_date = datetime.date(2024, 7, 10)  # 25 days from today

        result = weather_service._is_data_within_16_days(today, invalid_date)
        assert result is False

    def test_is_data_within_16_days_boundary(self, weather_service):
        """Test _is_data_within_16_days at the exact boundary"""
        today = datetime.date(2024, 6, 15)
        boundary_date = datetime.date(2024, 7, 1)  # Exactly 16 days from today

        result = weather_service._is_data_within_16_days(today, boundary_date)
        assert result is True

    @staticmethod
    def parametrize_cases():
        today = datetime.date.today()
        return [
            # Historical only
            (today - datetime.timedelta(days=20), today - datetime.timedelta(days=10), ("historical",)),
            # Forecast only
            (today + datetime.timedelta(days=5), today + datetime.timedelta(days=7), ("forecast",)),
            # Combined
            (today - datetime.timedelta(days=10), today + datetime.timedelta(days=3), ("historical", "forecast")),
        ]

    @pytest.mark.parametrize("start_date,end_date,expected_calls", parametrize_cases())
    def test_get_weather_different_date_ranges(
        self, weather_service, mock_weather_client, sample_hourly_data, start_date, end_date, expected_calls
    ):
        """Parametrized test for different date ranges"""
        request = WeatherRequest(
            latitude=40.7128, longitude=-74.0060, start_date=start_date, end_date=end_date, azimuth=180, tilt=30
        )

        mock_weather_client.fetch_historical_weather.return_value = sample_hourly_data
        mock_weather_client.fetch_forecast_weather.return_value = sample_hourly_data

        with patch("pandas.DataFrame") as mock_df:
            mock_df.return_value.to_dict.return_value = sample_hourly_data["hourly"]

            weather_service.get_weather(request)

        if "historical" in expected_calls:
            mock_weather_client.fetch_historical_weather.assert_called()
        else:
            mock_weather_client.fetch_historical_weather.assert_not_called()

        if "forecast" in expected_calls:
            mock_weather_client.fetch_forecast_weather.assert_called()
        else:
            mock_weather_client.fetch_forecast_weather.assert_not_called()

    def test_clock_integration(self, mock_weather_client):
        """Test that the clock function is properly used"""
        mock_clock = MagicMock(return_value=datetime.date(2024, 12, 1))
        service = WeatherService(mock_weather_client, clock=mock_clock)

        request = WeatherRequest(
            latitude=40.7128,
            longitude=-74.0060,
            start_date=datetime.date(2024, 12, 10),
            end_date=datetime.date(2024, 12, 15),
            azimuth=180,
            tilt=30,
        )

        mock_weather_client.fetch_forecast_weather.return_value = {"hourly": []}

        with patch("pandas.DataFrame") as mock_df:
            mock_df.return_value.to_dict.return_value = []
            service.get_weather(request)

        # Verify the mock clock was called
        mock_clock.assert_called()


# Integration test class for error scenarios
class TestWeatherServiceErrorScenarios:
    @pytest.fixture
    def weather_service_with_real_client(self):
        """Weather service with a real client for error testing"""
        mock_client = MagicMock(spec=WeatherClient)
        mock_clock = MagicMock(return_value=datetime.date(2024, 6, 15))
        return WeatherService(mock_client, clock=mock_clock)

    def test_client_exception_propagation(self, weather_service_with_real_client):
        """Test that client exceptions are properly propagated"""
        request = WeatherRequest(
            latitude=40.7128,
            longitude=-74.0060,
            start_date=datetime.date(2024, 6, 20),
            end_date=datetime.date(2024, 6, 25),
            azimuth=180,
            tilt=30,
        )

        # Mock client to raise an exception
        weather_service_with_real_client.weather_client.fetch_historical_weather.side_effect = (
            WeatherForecastAPILimitExceeded("API limit exceeded")
        )

        with pytest.raises(WeatherForecastAPILimitExceeded):
            weather_service_with_real_client.get_weather(request)
