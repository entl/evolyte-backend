from fastapi import APIRouter
from starlette import status

from src.auth.google.service import GoogleAuthProvider
from src.core.dependencies.auth import GoogleAuthServiceDep
from .schemas import GoogleOAuth2Response


google_auth_router = APIRouter(prefix="/auth/google", tags=["Google Auth"])


@google_auth_router.post("/login", status_code=status.HTTP_200_OK)
async def auth_user(oauth_info: GoogleOAuth2Response, google_auth_service: GoogleAuthServiceDep):
    token_pair = google_auth_service.authenticate(oauth_info=oauth_info)

    return token_pair
