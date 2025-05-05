from typing import Annotated

from fastapi import Depends


from .db import UowDep
from src.auth.service import AuthService


def auth_service(uow: UowDep):
    return AuthService(uow)


AuthServiceDep = Annotated[AuthService, Depends(auth_service)]
