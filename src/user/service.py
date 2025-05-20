from typing import List, Optional

from src.core.db.uow import UnitOfWork
from src.core.exceptions.user import (
    DuplicateEmailOrUsernameException,
    UserNotFoundException,
)
from src.core.utils import password_helper

from .models import User
from .schemas import UserCreate, UserResponse, UserUpdate


class UserService:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    def get_all_users(self) -> List[UserResponse]:
        users = self.uow.users.get_all()
        return [UserResponse.model_validate(user) for user in users]

    def get_user_by_id(self, user_id: int) -> Optional[UserResponse]:
        user = self.uow.users.get_by(id=user_id)
        return UserResponse.model_validate(user) if user else None

    def get_user_by_email(self, email: str) -> Optional[UserResponse]:
        user = self.uow.users.get_by(email=email)
        return UserResponse.model_validate(user) if user else None

    def create_user(self, user: UserCreate) -> UserResponse:
        with self.uow:
            # Check for duplicate username or email
            if self.uow.users.get_by(email=user.email):
                raise DuplicateEmailOrUsernameException()

            # Hash the password before storing
            hashed_password = password_helper.hash(user.password)
            user.password = hashed_password

            new_user = User(**user.model_dump(exclude={"password_confirmation"}))
            created_user = self.uow.users.create(new_user)

            return UserResponse.model_validate(created_user)

    def update_user(self, user_update: UserUpdate) -> UserResponse:
        with self.uow:
            # Retrieve the existing user
            user = self.uow.users.get_by(id=user_update.id)
            if not user:
                raise UserNotFoundException()

            # Update only provided fields
            update_data = user_update.model_dump(exclude_none=True, exclude_unset=True)
            for key, value in update_data.items():
                setattr(user, key, value)  # Update attributes dynamically

            updated_user = self.uow.users.update(user)

            return UserResponse.model_validate(updated_user)

    def is_admin(self, user_id: int) -> bool:
        user = self.uow.users.get_by(id=user_id)
        if not user:
            raise UserNotFoundException()

        if user.role == "admin":
            return True

        return False

    def delete_user(self, user_id: int) -> None:
        with self.uow:
            user = self.uow.users.get_by(id=user_id)
            if not user:
                raise UserNotFoundException()

            self.uow.users.delete(user)

    def logout(self) -> None:
        raise NotImplementedError("Logout functionality is not implemented yet.")
