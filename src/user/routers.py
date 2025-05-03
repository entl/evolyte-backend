from typing import Annotated

from fastapi import APIRouter, Depends, status
from pydantic import UUID4

from src.user.schemas import UserCreate, UserResponse, UserUpdate
from src.user.service import UserService

from src.core.exceptions.user import InsufficientPermissions, UserNotFoundException
from src.core.dependencies.permission import (
    PermissionDependencyHTTP,
    IsAuthenticated,
    IsAdmin,
    Permissions,
)
from src.core.dependencies.user import UserServiceDep
from src.schemas import CurrentUser

users_router = APIRouter(prefix="/users", tags=["Users"])


@users_router.get(
    "/",
    response_model=list[UserResponse],
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(PermissionDependencyHTTP([IsAuthenticated]))],
)
def get_all_users(user_service: UserServiceDep):
    """
    Get all users.

    This endpoint retrieves all users from the database.

    Args:
        user_service (UserService): User Service instance.

    Returns:
        list[UserResponse]: A list of all users in the database.
    """
    users = user_service.get_all_users()
    return users


@users_router.get(
    "/{user_id}",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(PermissionDependencyHTTP([IsAuthenticated]))],
)
def get_user_by_id(user_id: int, user_service: UserServiceDep):
    """
    Get user by ID.

    This endpoint retrieves a user from the database by their ID.

    Args:
        user_id (str): The ID of the user.
        user_service (UserService): User Service instance.

    Returns:
        UserResponse: The user with the specified ID.
    """
    user = user_service.get_user_by_id(user_id=user_id)
    if not user:
        raise UserNotFoundException()

    return user


@users_router.post(
    "/",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_user(user_service: UserServiceDep, user: UserCreate):
    """
    Create a new user.

    Args:
        user_service (UserService): User Service instance.
        user (UserCreate): User data to create.

    Returns:
        UserResponse: Created user data.
    """
    return user_service.create_user(user=user)


@users_router.patch(
    "/",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
)
def update_user(
    user_service: UserServiceDep,
    updated_user: UserUpdate,
    current_user: Annotated[
        CurrentUser, Depends(PermissionDependencyHTTP([IsAuthenticated, IsAdmin]))
    ],
):
    """
    Update a user.

    Args:
        user_service (UserService): User Service instance.
        updated_user (UserUpdate): User data to update.
        current_user (CurrentUser): The currently authenticated user.

    Returns:
        UserResponse: Updated user data.
    """
    if (
        current_user.id == updated_user.id
        or Permissions.IsAdmin in current_user.permissions
    ):
        return user_service.update_user(updated_user)
    else:
        raise InsufficientPermissions()


@users_router.delete(
    "/{user_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[]
)
def delete_user(
    user_service: UserServiceDep,
    user_id: UUID4,
    current_user: Annotated[
        CurrentUser, Depends(PermissionDependencyHTTP([IsAuthenticated, IsAdmin]))
    ],
):
    """
    Delete a user.

    Args:
        user_service (UserService): User Service instance.
        user_id (str): The ID of the user to delete.
        current_user (CurrentUser): The currently authenticated user.

    Returns:
        None
    """
    if current_user.id == user_id or Permissions.IsAdmin in current_user.permissions:
        user_service.delete_user(user_id=user_id)
    else:
        raise InsufficientPermissions()
