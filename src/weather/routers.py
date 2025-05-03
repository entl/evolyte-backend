from typing import Annotated

from fastapi import APIRouter, Query

from src.core.dependencies.weather import WeatherServiceDep
from src.weather.schemas import WeatherResponse, WeatherRequest

weather_router = APIRouter(prefix="/weather", tags=["Weather"])


@weather_router.get("", response_model=WeatherResponse)
def weather_forecast(
    request: Annotated[WeatherRequest, Query()], weather_service: WeatherServiceDep
):
    return weather_service.get_weather(request)
