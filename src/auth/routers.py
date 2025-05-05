from typing import Annotated

from fastapi import APIRouter, Depends, Request, Response, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status

from .schemas import TokenResponse, VerifyTokenRequest
from src.core.dependencies.auth import AuthServiceDep

auth_router = APIRouter(prefix="/auth", tags=["Auth"])


@auth_router.post("/refresh", response_model=TokenResponse)
def refresh_token(request: Request, response: Response, auth_service: AuthServiceDep):
    refresh_token = request.cookies.get("refresh_token")
    if not refresh_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Refresh token not found in cookies")

    token_pair = auth_service.refresh_tokens(refresh_token=refresh_token)

    response.set_cookie(
        key="refresh_token",
        value=token_pair.refresh_token,
        httponly=True,
        secure=True,
        samesite="lax",
        max_age=60 * 60 * 24 * 30,  # 30 days
    )

    return TokenResponse(access_token=token_pair.access_token)


@auth_router.post("/verify", status_code=status.HTTP_200_OK)
def verify_token(request: VerifyTokenRequest, auth_service: AuthServiceDep):
    auth_service.verify_access_token(token=request.token)
    return {"valid": True}


@auth_router.post("/login", response_model=TokenResponse, status_code=status.HTTP_200_OK)
def login(
    response: Response,
    user_credentials: Annotated[OAuth2PasswordRequestForm, Depends()],
    auth_service: AuthServiceDep,
):
    token_pair = auth_service.login(email=user_credentials.username, password=user_credentials.password)

    response.set_cookie(
        key="refresh_token",
        value=token_pair.refresh_token,
        httponly=True,
        secure=True,
        samesite="lax",
        max_age=60 * 60 * 24 * 30,  # 30 days
    )

    return TokenResponse(access_token=token_pair.access_token)
