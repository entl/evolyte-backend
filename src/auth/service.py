from src.core.db.uow import UnitOfWork
from src.core.exceptions.user import UserNotFoundException, PasswordDoesNotMatchException
from src.core.utils import password_helper
from src.core.utils.token_helper import TokenHelper
from src.auth.schemas import TokenPair, TokenPayload

from src.core.exceptions.token import TokenValidationError


class AuthService:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow
        self._token_helper = TokenHelper()
        self._access_token_expiry = 60 * 60  # 1 hour
        self._refresh_token_expiry = 60 * 60 * 24 * 30  # 30 days

    def create_token_pair(self, user_id: int) -> TokenPair:
        access_payload = {
            "user_id": user_id,
            "sub": "access",
        }

        refresh_payload = {
            "user_id": user_id,
            "sub": "refresh",
        }

        access_token = self._token_helper.encode(access_payload, self._access_token_expiry)
        refresh_token = self._token_helper.encode(refresh_payload, self._refresh_token_expiry)

        return TokenPair(
            access_token=access_token,
            refresh_token=refresh_token,
        )

    def verify_access_token(self, token: str) -> TokenPayload:
        payload = self._token_helper.decode(token)
        if payload.get("sub") != "access":
            raise TokenValidationError("Invalid access token scope")
        return TokenPayload(**payload)

    def refresh_tokens(self, refresh_token: str) -> TokenPair:
        payload = self._token_helper.decode(refresh_token)
        if payload.get("sub") != "refresh":
            raise TokenValidationError("Invalid refresh token scope")

        user_id = payload.get("user_id")
        if not user_id:
            raise TokenValidationError("Missing user_id in refresh token")

        return self.create_token_pair(user_id=user_id)

    def login(self, email: str, password: str) -> TokenPair:
        user = self.uow.users.get_by(email=email)

        if not user:
            raise UserNotFoundException()
        if not password_helper.verify(password, user.password):
            raise PasswordDoesNotMatchException()

        return self.create_token_pair(user_id=user.id)
