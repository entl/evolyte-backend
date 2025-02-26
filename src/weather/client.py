from abc import ABC, abstractmethod
from datetime import datetime

import requests


class WeatherClient(ABC):
    @abstractmethod
    def fetch_weather_data(self, latitude, longitude, start_date, end_date, azimuth, tilt) -> dict:
        pass


class OpenMeteoClient(WeatherClient):
    BASE_URL = "https://archive-api.open-meteo.com/v1/archive"

    FIXED_PARAMS = {
        "hourly": ",".join([
            "temperature_2m",
            "apparent_temperature",
            "relative_humidity_2m",
            "dew_point_2m",
            "pressure_msl",
            "surface_pressure",
            "precipitation",
            "cloud_cover",
            "et0_fao_evapotranspiration",
            "wind_speed_10m",
            "wind_direction_10m",
            "shortwave_radiation",
            "diffuse_radiation",
            "direct_radiation",
            "direct_normal_irradiance",
            "terrestrial_radiation",
            "is_day",
            "sunshine_duration"
        ])
    }

    def fetch_weather_data(self, latitude: float, longitude: float, start_date: datetime, end_date: datetime, azimuth: float, tilt: float) -> dict:
        params = {
            **self.FIXED_PARAMS,
            "latitude": latitude,
            "longitude": longitude,
            "start_date": str(start_date),
            "end_date": str(end_date),
            "azimuth": azimuth,
            "tilt": tilt,
        }

        try:
            response = requests.get(self.BASE_URL, params=params, timeout=10)
            response.raise_for_status()
            return response.json()

        except requests.RequestException as e:
            raise RuntimeError(f"Failed to fetch weather data: {e}")