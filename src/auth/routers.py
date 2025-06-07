from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status

from .schemas import VerifyTokenRequest, RefreshTokenRequest, TokenPairResponse
from src.core.dependencies.auth import AuthServiceDep
from src.logger import get_logger

auth_router = APIRouter(prefix="/auth", tags=["Auth"])

# Configure logger for this module
auth_logger = get_logger(__name__)


@auth_router.post("/refresh", response_model=TokenPairResponse)
def refresh_token(request: RefreshTokenRequest, auth_service: AuthServiceDep):
    auth_logger.info(f"Refreshing access token for refresh_token: {request.refresh_token}")
    access_token = auth_service.refresh_access_token(refresh_token=request.refresh_token)
    auth_logger.info("Access token refreshed successfully")
    return TokenPairResponse(access_token=access_token, refresh_token=request.refresh_token)


@auth_router.post("/verify", status_code=status.HTTP_200_OK)
def verify_token(request: VerifyTokenRequest, auth_service: AuthServiceDep):
    auth_logger.info("Verifying access token")
    auth_service.verify_access_token(token=request.access_token)
    auth_logger.info("Access token is valid")
    return {"valid": True}


@auth_router.post("/login", response_model=TokenPairResponse, status_code=status.HTTP_200_OK)
def login(
    user_credentials: Annotated[OAuth2PasswordRequestForm, Depends()],
    auth_service: AuthServiceDep,
):
    auth_logger.info(f"User login attempt: {user_credentials.username}")
    token_pair = auth_service.login(email=user_credentials.username, password=user_credentials.password)
    auth_logger.info(f"User logged in successfully: {user_credentials.username}")
    return TokenPairResponse(access_token=token_pair.access_token, refresh_token=token_pair.refresh_token)
