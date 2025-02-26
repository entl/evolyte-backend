from pydantic import BaseModel, Field
from datetime import date
from typing import List


class WeatherRequest(BaseModel):
    latitude: float = Field(..., example=51.5074)
    longitude: float = Field(..., example=-0.1278)
    azimuth: float = Field(..., example=180.0)
    tilt: float = Field(..., example=30.0)
    start_date: date = Field(..., example="2024-01-01")
    end_date: date = Field(..., example="2024-01-10")


class HourlyWeatherData(BaseModel):
    # Schema for hourly weather data response
    time: str
    temperature_2m: float
    apparent_temperature: float
    relative_humidity_2m: float
    dew_point_2m: float
    pressure_msl: float
    surface_pressure: float
    precipitation: float
    cloud_cover: float
    et0_fao_evapotranspiration: float
    wind_speed_10m: float
    wind_direction_10m: float
    shortwave_radiation: float
    diffuse_radiation: float
    direct_radiation: float
    direct_normal_irradiance: float
    terrestrial_radiation: float
    is_day: int
    sunshine_duration: float


class WeatherResponse(BaseModel):
    latitude: float
    longitude: float
    start_date: date
    end_date: date
    hourly: List[HourlyWeatherData]
