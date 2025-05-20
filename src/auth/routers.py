from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status

from .schemas import VerifyTokenRequest, RefreshTokenRequest, TokenPairResponse
from src.core.dependencies.auth import AuthServiceDep

auth_router = APIRouter(prefix="/auth", tags=["Auth"])


@auth_router.post("/refresh", response_model=TokenPairResponse)
def refresh_token(request: RefreshTokenRequest, auth_service: AuthServiceDep):
    access_token = auth_service.refresh_access_token(refresh_token=request.refresh_token)

    return TokenPairResponse(access_token=access_token, refresh_token=request.refresh_token)


@auth_router.post("/verify", status_code=status.HTTP_200_OK)
def verify_token(request: VerifyTokenRequest, auth_service: AuthServiceDep):
    auth_service.verify_access_token(token=request.token)
    return {"valid": True}


@auth_router.post("/login", response_model=TokenPairResponse, status_code=status.HTTP_200_OK)
def login(
    user_credentials: Annotated[OAuth2PasswordRequestForm, Depends()],
    auth_service: AuthServiceDep,
):
    token_pair = auth_service.login(email=user_credentials.username, password=user_credentials.password)

    return TokenPairResponse(access_token=token_pair.access_token, refresh_token=token_pair.refresh_token)
