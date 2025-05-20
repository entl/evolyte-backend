from datetime import datetime, timedelta

from google.oauth2 import id_token
from google.auth.transport import requests
from google.auth.exceptions import GoogleAuthError

from src.auth.service import AuthProvider, AuthService
from src.auth.schemas import TokenPairResponse, TokenPayload
from src.auth.models import Identity
from src.user.models import User
from src.core.db.uow import UnitOfWork
from src.core.exceptions.token import TokenValidationError
from src.core.exceptions.user import UserNotFoundException
from src.settings import settings
from .schemas import GoogleOAuth2Response


class GoogleAuthProvider(AuthProvider):
    def __init__(self, uow: UnitOfWork, auth_service: AuthService):
        self.uow = uow
        self.auth_service = auth_service

    def verify_access_token(self, token: str) -> TokenPayload:
        # Implement Google-specific logic to verify access token
        pass

    def refresh_access_token(self, refresh_token: str) -> str:
        pass

    def authenticate(self, oauth_info: GoogleOAuth2Response) -> TokenPairResponse:
        # verify the ID token
        self.verify_id_token(oauth_info.tokens.id_token)

        identity = self.uow.identities.get_by(provider_user_id=oauth_info.user.sub)
        user = self.uow.users.get_by(email=oauth_info.user.email)

        # probably some issues with consistency, since identity can't exist without user
        if identity and not user:
            raise UserNotFoundException("User with this identity does not exist. Please link your account first.")

        # new user
        if not user and not identity:
            # create a new user
            with self.uow as uow:
                # TODO: add check so password can be null, only when creating user with oauth
                new_user = User(email=oauth_info.user.email, full_name=oauth_info.user.name, password=None)
                created_user = uow.users.create(new_user)

                # get expiration time from the token, deduct 60 seconds to prevent edge cases
                # TODO: fetch created at from the token
                expires_at = self._calculate_expiration_time(oauth_info.tokens.expires_in)
                new_identity = self._perform_identity_linking(
                    uow=uow,
                    user_id=created_user.id,
                    provider="google",
                    provider_user_id=oauth_info.user.sub,
                    access_token=oauth_info.tokens.access_token,
                    expires_at=expires_at,
                )

                self.uow.commit()

            return self.auth_service.create_token_pair(created_user.id)

        # user exists but not linked to identity
        if user and not identity:
            # user exists but not linked to identity
            with self.uow as uow:
                expires_at = self._calculate_expiration_time(oauth_info.tokens.expires_in)
                self._perform_identity_linking(
                    uow,
                    user_id=user.id,
                    provider="google",
                    provider_user_id=oauth_info.user.sub,
                    access_token=oauth_info.tokens.access_token,
                    expires_at=expires_at,
                )

            return self.auth_service.create_token_pair(user.id)

        # if user AND identity exist, just return the token pair
        if user and identity:
            return self.auth_service.create_token_pair(user.id)

    def verify_id_token(self, token: str):
        try:
            id_token.verify_oauth2_token(token, requests.Request(), audience=settings.google_client_id)
        except GoogleAuthError as e:
            print("GoogleAuthError", e)
            raise TokenValidationError("Invalid ID token")

    def get_user_info(self, token: str) -> dict:
        pass

    def link_identity(self, oauth_info: GoogleOAuth2Response, provider) -> None:
        with self.uow:
            identity = self.uow.identities.get_by(provider_user_id=oauth_info.user.sub)
            if identity:
                raise UserNotFoundException("Identity already exists")

            new_identity = self._perform_identity_linking(
                uow=self.uow,
                user_id=oauth_info.user.user_id,
                provider=provider,
                provider_user_id=oauth_info.user.sub,
                access_token=oauth_info.tokens.access_token,
                expires_at=None,
            )

            self.uow.commit()

    def unlink_identity(self, user_id: int, provider: str) -> None:
        pass

    def rotate_refresh_token(self, refresh_token: str) -> str:
        pass

    def _perform_identity_linking(
        self,
        uow: UnitOfWork,
        user_id: int,
        provider: str,
        provider_user_id: str,
        access_token: str,
        expires_at: datetime,
    ) -> Identity:
        identity = Identity(
            user_id=user_id,
            provider=provider,
            provider_user_id=provider_user_id,
            access_token=access_token,
            expires_at=expires_at,
        )

        created_identity = uow.identities.create(identity)

        return created_identity

    def _calculate_expiration_time(self, expires_in: int) -> datetime:
        # get expiration time from the token, deduct 60 seconds to prevent edge cases
        return timedelta(seconds=expires_in - 60) + datetime.now()
