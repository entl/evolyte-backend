from typing import Annotated

from fastapi import APIRouter, Query

from src.core.dependencies.weather import WeatherServiceDep
from src.weather.schemas import WeatherRequest, WeatherResponse

from src.logger import get_logger

weather_router = APIRouter(prefix="/weather", tags=["Weather"])

weather_logger = get_logger(__name__)


@weather_router.get("", response_model=WeatherResponse)
def weather_forecast(request: Annotated[WeatherRequest, Query()], weather_service: WeatherServiceDep):
    weather_logger.info(f"Weather forecast request received: {request}")
    result = weather_service.get_weather(request)
    weather_logger.info("Weather forecast completed successfully")
    return result
