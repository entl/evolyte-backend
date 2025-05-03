import requests

from src.predict.schemas import (
    PredictionClientRequest,
    PredictionClientResponse,
    BatchPredictionClientRequest,
    BatchPredictionClientResponse,
)
from src.settings import settings


class PredictionClient:
    def __init__(self):
        self.base_url = settings.ml_api_url

    def predict(self, request: PredictionClientRequest) -> PredictionClientResponse:
        try:
            response = requests.post(
                f"{self.base_url}/prediction/predict",
                json=request.model_dump(mode="json"),
                headers={"Content-Type": "application/json"},
            )
            response.raise_for_status()
            return PredictionClientResponse(**response.json())
        except requests.RequestException as e:
            raise RuntimeError(f"Failed to fetch prediction: {e}")

    def batch_predict(
        self, request: BatchPredictionClientRequest
    ) -> BatchPredictionClientResponse:
        try:
            response = requests.post(
                f"{self.base_url}/prediction/batch-predict",
                json=request.model_dump(mode="json"),
                headers={"Content-Type": "application/json"},
            )
            response.raise_for_status()
            test = BatchPredictionClientResponse.model_validate(
                response.json(), from_attributes=True
            )
            return test
        except requests.RequestException as e:
            raise RuntimeError(f"Failed to fetch batch prediction: {e}")
