from typing import Annotated

from fastapi import Depends


from .db import UowDep
from src.auth.service import AuthService
from src.auth.google.service import GoogleAuthProvider


def auth_service(uow: UowDep):
    return AuthService(uow)


AuthServiceDep = Annotated[AuthService, Depends(auth_service)]


def google_auth_service(uow: UowDep, auth_service: AuthServiceDep):
    return GoogleAuthProvider(uow=uow, auth_service=auth_service)


GoogleAuthServiceDep = Annotated[GoogleAuthProvider, Depends(google_auth_service)]
