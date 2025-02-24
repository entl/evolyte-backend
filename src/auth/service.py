from .schemas import RefreshTokenBase

from src.core.exceptions.token import DecodeTokenException
from src.core.utils.token_helper import TokenHelper


class JwtService:
    def verify_token(self, token: str) -> None:
        TokenHelper.decode(token=token)

    def create_refresh_token(
        self,
        token: str,
        refresh_token: str,
    ) -> RefreshTokenBase:
        token = TokenHelper.decode(token=token)
        refresh_token = TokenHelper.decode(token=refresh_token)
        if refresh_token.get("sub") != "refresh":
            raise DecodeTokenException

        return RefreshTokenBase(
            access_token=TokenHelper.encode(payload={"user_id": token.get("user_id")}),
            refresh_token=TokenHelper.encode(payload={"sub": "refresh"}),
            token_type="bearer",
        )
