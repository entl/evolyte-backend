from typing import Annotated

from fastapi import APIRouter, Query

from src.core.dependencies.prediction import PredictionServiceDep
from src.logger import get_logger
from src.predict.schemas import (
    BatchPredictionRequest,
    BatchPredictionResponse,
    PredictionRequest,
    PredictionResponse,
    TimeSeriesPredictionRequest,
)

predict_router = APIRouter(prefix="/predict", tags=["Predict"])

# Configure logger for this module
predict_logger = get_logger(__name__)


@predict_router.get("/", response_model=PredictionResponse)
def predict_solar_panel_output(
    request: Annotated[PredictionRequest, Query()],
    prediction_service: PredictionServiceDep,
):
    predict_logger.info(f"Predicting solar panel output for request: {request}")
    result = prediction_service.predict(request)
    predict_logger.info("Prediction completed successfully")
    return result


@predict_router.post("/batch", response_model=BatchPredictionResponse)
def predict_solar_panel_output_batch(request: BatchPredictionRequest, prediction_service: PredictionServiceDep):
    predict_logger.info(f"Batch prediction request received: {request}")
    result = prediction_service.predict_batch(request)
    predict_logger.info("Batch prediction completed successfully")
    return result


@predict_router.post("/time-series", response_model=BatchPredictionResponse)
def predict_solar_panel_output_time_series(
    request: TimeSeriesPredictionRequest, prediction_service: PredictionServiceDep
):
    predict_logger.info(f"Time series prediction request received: {request}")
    result = prediction_service.predict_time_series(request)
    predict_logger.info("Time series prediction completed successfully")
    return result
