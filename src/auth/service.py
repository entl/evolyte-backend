from abc import ABC, abstractmethod

from src.core.db.uow import UnitOfWork
from src.core.exceptions.user import UserNotFoundException, PasswordDoesNotMatchException
from src.core.utils import password_helper
from src.core.utils.token_helper import TokenHelper
from src.auth.schemas import TokenPairResponse, TokenPayload
from src.core.exceptions.token import TokenValidationError
from src.settings import settings


class AuthService:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow
        self._token_helper = TokenHelper()
        self._access_token_expiry = settings.jwt_token_expiration_time
        self._refresh_token_expiry = settings.jwt_refresh_token_expiration_time

    def create_token_pair(self, user_id: int) -> TokenPairResponse:
        access_token = self._create_access_token(user_id=user_id)
        refresh_token = self._create_refresh_token(user_id=user_id)

        return TokenPairResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer",
        )

    def verify_access_token(self, token: str) -> TokenPayload:
        payload = self._token_helper.decode(token)
        if payload.get("sub") != "access":
            raise TokenValidationError("Invalid access token scope")
        return TokenPayload(**payload)

    def refresh_access_token(self, refresh_token: str) -> str:
        payload = self._token_helper.decode(refresh_token)
        if payload.get("sub") != "refresh":
            raise TokenValidationError("Invalid refresh token scope")

        user_id = payload.get("user_id")
        if not user_id:
            raise TokenValidationError("Missing user_id in refresh token")

        return self._create_access_token(user_id=user_id)

    def login(self, email: str, password: str) -> TokenPairResponse:
        user = self.uow.users.get_by(email=email)

        if not user:
            raise UserNotFoundException()
        if not password_helper.verify(password, user.password):
            raise PasswordDoesNotMatchException()

        return self.create_token_pair(user_id=user.id)

    def _create_access_token(self, user_id: int) -> str:
        payload = {
            "user_id": user_id,
            "sub": "access",
        }
        return self._token_helper.encode(payload, self._access_token_expiry)

    def _create_refresh_token(self, user_id: int) -> str:
        payload = {
            "user_id": user_id,
            "sub": "refresh",
        }
        return self._token_helper.encode(payload, self._refresh_token_expiry)


class AuthProvider(ABC):
    @abstractmethod
    def refresh_access_token(self, refresh_token: str) -> str:
        pass

    @abstractmethod
    def verify_access_token(self, token: str) -> TokenPayload:
        pass

    @abstractmethod
    def verify_id_token(self, token: str) -> dict:
        pass

    @abstractmethod
    def get_user_info(self, token: str) -> dict:
        pass

    @abstractmethod
    def authenticate(self, oauth_info) -> TokenPairResponse:
        pass

    @abstractmethod
    def link_identity(self, oauth_info, provider: str) -> None:
        pass

    @abstractmethod
    def unlink_identity(self, user_id: int, provider: str) -> None:
        pass

    @abstractmethod
    def rotate_refresh_token(self, refresh_token: str) -> str:
        pass
