from src.core.exceptions.base import CustomException


class TokenException(CustomException):
    pass


class DecodeTokenException(TokenException):
    code = 400
    error_code = "TOKEN__DECODE_ERROR"
    message = "Token decode error"


class ExpiredTokenException(TokenException):
    code = 400
    error_code = "TOKEN__EXPIRE_ERROR"
    message = "JWT token has expired"
