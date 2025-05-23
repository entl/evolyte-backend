from typing import Annotated

from fastapi import Depends

from src.weather.client import OpenMeteoClient
from src.weather.service import WeatherService


def weather_client():
    return OpenMeteoClient()


WeatherClientDep = Annotated[OpenMeteoClient, Depends(weather_client)]


def weather_service(weather_client: WeatherClientDep):
    return WeatherService(weather_client)


WeatherServiceDep = Annotated[WeatherService, Depends(weather_service)]
