from typing import Tuple

from starlette.authentication import AuthenticationBackend
from starlette.middleware.authentication import (
    AuthenticationMiddleware as BaseAuthenticationMiddleware,
)
from starlette.requests import HTTPConnection

from src.core.exceptions.token import TokenException
from src.core.utils.token_helper import TokenHelper
from src.schemas import CurrentUser
from src.user.schemas import UserRoles


# class AuthBackend(AuthenticationBackend):
#     async def authenticate(self, conn: HTTPConnection) -> Tuple[bool, CurrentUser]:
#         current_user = CurrentUser()
#         authorization: str | None = conn.headers.get("Authorization")
#         if not authorization:
#             return False, current_user

#         try:
#             token_type, payload_encoded = authorization.split(" ")
#             if token_type.lower() != "bearer":
#                 return False, current_user
#         except ValueError:
#             return False, current_user

#         if not payload_encoded:
#             return False, current_user

#         try:
#             payload = TokenHelper.decode(payload_encoded)
#             user_id = payload.get("user_id")
#         except TokenException:
#             return False, current_user

#         current_user.id = user_id
#         return True, current_user


class AuthBackend(AuthenticationBackend):
    async def authenticate(self, conn: HTTPConnection) -> Tuple[bool, CurrentUser]:
        current_user = CurrentUser()
        user_id: str | None = conn.headers.get("X-User-ID")
        role: UserRoles | str | None = conn.headers.get("X-User-Role")
        if not user_id:
            return False, current_user
        
        if not role:
            return False, current_user
        
        current_user.id = user_id
        current_user.role = role

        return True, current_user


class AuthenticationMiddleware(BaseAuthenticationMiddleware):
    pass
