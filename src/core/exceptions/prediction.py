from http import HTTPStatus
from src.core.exceptions.base import CustomException


class PredictionException(CustomException):
    code = HTTPStatus.BAD_REQUEST
    error_code = HTTPStatus.BAD_REQUEST
    message = "Prediction request failed due to an error."


class BatchPredictionException(CustomException):
    code = HTTPStatus.BAD_REQUEST
    error_code = HTTPStatus.BAD_REQUEST
    message = "Batch prediction request failed due to an error."
