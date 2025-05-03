from typing import Annotated

from fastapi import Depends

from src.core.db.session import SessionFactory
from src.user.repository import UserRepository
from src.user.service import UserService

from .db import UowDep


def user_repository():
    return UserRepository(SessionFactory())


UserRepositoryDep = Annotated[UserRepository, Depends(user_repository)]


def user_service(uow: UowDep):
    return UserService(uow)


UserServiceDep = Annotated[UserService, Depends(user_service)]
