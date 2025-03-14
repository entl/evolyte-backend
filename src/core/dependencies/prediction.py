from typing import Annotated

from fastapi import Depends

from src.core.dependencies.weather import WeatherServiceDep
from src.predict.service import PredictionService
from src.predict.client import PredictionClient


def prediction_client():
    return PredictionClient()


PredictionClientDep = Annotated[PredictionClient, Depends(prediction_client)]


def prediction_service(prediction_client: PredictionClientDep, weather_service: WeatherServiceDep):
    return PredictionService(weather_service=weather_service, prediction_client=prediction_client)


PredictionServiceDep = Annotated[PredictionService, Depends(prediction_service)]


