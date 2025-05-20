from fastapi import APIRouter, Request, HTTPException
from starlette import status

from src.auth.schemas import VerifyTokenRequest, RefreshTokenRequest, TokenPairResponse
from src.core.dependencies.auth import AuthServiceDep
from src.auth.google.service import GoogleAuthProvider
from src.core.dependencies.db import UowDep
from .schemas import GoogleOAuth2Response


google_auth_router = APIRouter(prefix="/auth/google", tags=["Google Auth"])


@google_auth_router.post("/login", status_code=status.HTTP_200_OK)
async def auth_user(oauth_info: GoogleOAuth2Response, uow: UowDep, auth_service: AuthServiceDep):
    google_auth = GoogleAuthProvider(uow=uow, auth_service=auth_service)
    token_pair = google_auth.authenticate(oauth_info=oauth_info)

    return token_pair
