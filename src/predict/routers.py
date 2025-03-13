from typing import Annotated

from fastapi import APIRouter, Query

from src.core.dependencies.prediction import PredictionServiceDep
from src.predict.schemas import PredictionRequest, PredictionResponse, BatchPredictionRequest, BatchPredictionResponse, TimeSeriesPredictionRequest

predict_router = APIRouter(prefix="/predict", tags=["Predict"])


@predict_router.get("/", response_model=PredictionResponse)
def predict_solar_panel_output(request: Annotated[PredictionRequest, Query()], prediction_service: PredictionServiceDep):
    return prediction_service.predict(request)


@predict_router.post("/batch", response_model=BatchPredictionResponse)
def predict_solar_panel_output_batch(request: BatchPredictionRequest, prediction_service: PredictionServiceDep):
    return prediction_service.predict_batch(request)


@predict_router.post("/time-series", response_model=BatchPredictionResponse)
def predict_solar_panel_output_time_series(request: TimeSeriesPredictionRequest, prediction_service: PredictionServiceDep):
    return prediction_service.predict_time_series(request)


