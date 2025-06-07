from typing import Annotated

from fastapi import APIRouter, Depends, status

from src.core.dependencies.permission import (
    IsAdmin,
    IsAuthenticated,
    PermissionDependencyHTTP,
    Permissions,
)
from src.core.dependencies.user import UserServiceDep
from src.core.exceptions.user import InsufficientPermissions, UserNotFoundException
from src.schemas import CurrentUser
from src.user.schemas import UserCreate, UserResponse, UserUpdate
from src.logger import get_logger

# Configure logger for this module
logger = get_logger(__name__)

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
    logger.info("Fetching all users")
    users = user_service.get_all_users()
    logger.info(f"Found {len(users)} users")
    return users


@users_router.get(
    "/me",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(PermissionDependencyHTTP([IsAuthenticated]))],
)
def get_current_user(
    user_service: UserServiceDep,
    current_user: Annotated[CurrentUser, Depends(PermissionDependencyHTTP([IsAuthenticated]))],
):
    """
    Get current user.

    This endpoint retrieves the currently authenticated user.

    Args:
        user_service (UserService): User Service instance.
        current_user (CurrentUser): The currently authenticated user.

    Returns:
        UserResponse: The currently authenticated user.
    """
    logger.info(f"Fetching current user: {current_user.id}")
    return user_service.get_user_by_id(user_id=current_user.id)


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
    logger.info(f"Fetching user by ID: {user_id}")
    user = user_service.get_user_by_id(user_id=user_id)
    if not user:
        logger.warning(f"User not found: {user_id}")
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
    logger.info(f"Creating user: {getattr(user, 'email', user)}")
    created_user = user_service.create_user(user=user)
    logger.info(f"User created with ID: {created_user.id}")
    return created_user


@users_router.patch(
    "/",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
)
def update_user(
    user_service: UserServiceDep,
    updated_user: UserUpdate,
    current_user: Annotated[CurrentUser, Depends(PermissionDependencyHTTP([IsAuthenticated, IsAdmin]))],
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
    logger.info(f"Updating user: {updated_user.id} by {current_user.id}")
    if current_user.id == updated_user.id or Permissions.IsAdmin in current_user.permissions:
        updated = user_service.update_user(updated_user)
        logger.info(f"User updated: {updated_user.id}")
        return updated
    else:
        logger.warning(f"Insufficient permissions for user: {current_user.id} to update {updated_user.id}")
        raise InsufficientPermissions()


@users_router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[])
def delete_user(
    user_service: UserServiceDep,
    user_id: int,
    current_user: Annotated[CurrentUser, Depends(PermissionDependencyHTTP([IsAuthenticated, IsAdmin]))],
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
    logger.info(f"Deleting user: {user_id} by {current_user.id}")
    if current_user.id == user_id or Permissions.IsAdmin in current_user.permissions:
        user_service.delete_user(user_id=user_id)
        logger.info(f"User deleted: {user_id}")
    else:
        logger.warning(f"Insufficient permissions for user: {current_user.id} to delete {user_id}")
        raise InsufficientPermissions()
