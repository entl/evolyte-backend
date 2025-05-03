from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status

from .schemas import RefreshTokenRequest, RefreshTokenResponse, VerifyTokenRequest
from .service import JwtService
from src.user.schemas import LoginResponse
from src.core.dependencies.user import UserServiceDep

auth_router = APIRouter(prefix="/auth", tags=["Auth"])


@auth_router.post(
    "/refresh",
    response_model=RefreshTokenResponse,
)
def refresh_token(request: RefreshTokenRequest):
    token = JwtService().create_refresh_token(
        token=request.token, refresh_token=request.refresh_token
    )
    return {"token": token.token, "refresh_token": token.refresh_token}


@auth_router.post("/verify", status_code=status.HTTP_200_OK)
def verify_token(request: VerifyTokenRequest):
    JwtService().verify_token(token=request.token)


@auth_router.post(
    "/login", response_model=LoginResponse, status_code=status.HTTP_200_OK
)
def login(
    user_credentials: Annotated[OAuth2PasswordRequestForm, Depends()],
    user_service: UserServiceDep,
):
    token = user_service.login(
        email=user_credentials.username, password=user_credentials.password
    )
    return token
