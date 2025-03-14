from fastapi import status

from src.core.exceptions.base import CustomException


class WeatherForecastExceedsMaxFutureDate(CustomException):
    code = status.HTTP_400_BAD_REQUEST
    error_code = "WEATHER__FORECAST_EXCEEDS_MAX_FUTURE_DATE"
    message = "Forecast can be made only 16 days advance."


class WeatherForecastAPILimitExceeded(CustomException):
    code = status.HTTP_400_BAD_REQUEST
    error_code = "WEATHER__FORECAST_API_LIMIT_EXCEEDED"
    message = "API limit exceeded."
