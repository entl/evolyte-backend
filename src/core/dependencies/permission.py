from abc import ABC, abstractmethod
from typing import List, Type

from fastapi import Request
from fastapi.openapi.models import APIKey, APIKeyIn
from fastapi.security.base import SecurityBase

from src.user.repository import UserRepository
from src.user.service import UserService
from src.core.exceptions.base import CustomException, UnauthorizedException
from src.schemas import CurrentUser
from src.core.db.session import SessionFactory


class Permissions:
    IsAuthenticated = "IsAuthenticated"
    IsAdmin = "IsAdmin"
    AllowAll = "AllowAll"


class BasePermission(ABC):
    exception = CustomException
    alias: str = None

    @abstractmethod
    def has_permission(self, request: Request) -> bool:
        pass


class IsAuthenticated(BasePermission):
    exception = UnauthorizedException
    alias = Permissions.IsAuthenticated

    def has_permission(self, request: Request) -> bool:
        return request.user.id is not None


class IsAdmin(BasePermission):
    exception = UnauthorizedException
    alias = Permissions.IsAdmin

    def has_permission(self, request: Request) -> bool:
        user_id = request.user.id
        if not user_id:
            return False

        return UserService(UserRepository(SessionFactory())).is_admin(user_id=user_id)


class PermissionDependencyBase(SecurityBase, ABC):
    @abstractmethod
    def __call__(self, request: Request) -> CurrentUser:
        pass
    
    @abstractmethod
    def is_user_has_any_permissions(self, request: Request) -> List[str]:
        pass


class PermissionDependencyHTTP(PermissionDependencyBase):
    def __init__(self, permissions: List[Type[BasePermission]]):
        self.permissions = permissions

        self.model: APIKey = APIKey(**{"in": APIKeyIn.header}, name="Authorization")
        self.scheme_name = self.__class__.__name__

    def __call__(self, request: Request):
        # Admin users bypass permission checks
        if getattr(request.user, "is_admin", False):
            return CurrentUser(id=request.user.id, permissions=["admin"])

        # For non-admin users, ensure they have at least one of the required permissions
        allowed_permissions = self.is_user_has_any_permissions(request=request)
        return CurrentUser(id=request.user.id, permissions=allowed_permissions)

    def is_user_has_any_permissions(self, request: Request) -> List[str]:
        allowed_permissions = []
        # Check each permission. If at least one is granted, we allow access.
        for permission_cls in self.permissions:
            permission_instance = permission_cls()
            if permission_instance.has_permission(request=request):
                allowed_permissions.append(permission_instance.alias)
        if allowed_permissions:
            return allowed_permissions
        raise UnauthorizedException("Insufficient permissions.")
