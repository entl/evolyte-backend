from fastapi import status

from src.core.exceptions.base import CustomException


class SolarPanelNotFoundException(CustomException):
    code = status.HTTP_404_NOT_FOUND
    error_code = "USER__SOLAR_PANEL_NOT_FOUND"
    message = "Solar panel not found."
