from typing import Optional, List
from pydantic import UUID4
from sqlalchemy.orm import Session
from .repository import UserRepository
from .schemas import UserOut, UserCreate, UserUpdate, LoginResponse
from .models import User
from src.core import exceptions
from src.core.utils import password_helper
from src.core.utils.token_helper import TokenHelper


class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def get_all_users(self) -> List[UserOut]:
        users = self.user_repository.get_all()
        return [UserOut.model_validate(user) for user in users]

    def get_user_by_id(self, user_id: UUID4) -> Optional[UserOut]:
        user = self.user_repository.get_by_id(user_id)
        return UserOut.model_validate(user) if user else None

    def get_user_by_username(self, username: str) -> Optional[UserOut]:
        user = self.user_repository.get_by_username(username)
        return UserOut.model_validate(user) if user else None

    def get_user_by_email(self, email: str) -> Optional[UserOut]:
        user = self.user_repository.get_by_email(email)
        return UserOut.model_validate(user) if user else None

    def create_user(self, user: UserCreate) -> UserOut:
        try:
            # Check for duplicate username or email
            if self.get_user_by_username(user.username):
                raise exceptions.user.DuplicateEmailOrNicknameException()
            if self.get_user_by_email(user.email):
                raise exceptions.user.DuplicateEmailOrNicknameException()

            # Hash the password before storing
            hashed_password = password_helper.hash(user.password)
            user.password = hashed_password

            new_user = User(**user.model_dump())
            created_user = self.user_repository.create(new_user)

            self.db_session.commit()  # Commit transaction
            self.db_session.refresh(created_user)  # Ensure the latest data is reflected

            return UserOut.model_validate(created_user)
        except Exception as e:
            self.db_session.rollback()  # Rollback in case of failure
            raise e

    def update_user(self, user_update: UserUpdate) -> UserOut:
        try:
            # Retrieve the existing user
            user = self.user_repository.get_by_id(user_update.id)
            if not user:
                raise exceptions.user.UserNotFoundException()

            # Update only provided fields
            update_data = user_update.model_dump(exclude_none=True, exclude_unset=True)
            for key, value in update_data.items():
                setattr(user, key, value)  # Update attributes dynamically

            updated_user = self.user_repository.update(user)

            self.db_session.commit()  # Commit transaction
            self.db_session.refresh(updated_user)  # Ensure up-to-date state

            return UserOut.model_validate(updated_user)
        except Exception as e:
            self.db_session.rollback()
            raise e

    def login(self, email: str, password: str) -> LoginResponse:
        user = self.user_repository.get_by_email(email)
        if not user:
            raise exceptions.user.UserNotFoundException()
        if not password_helper.verify(password, user.password):
            raise exceptions.user.PasswordDoesNotMatchException()

        return LoginResponse(
            access_token=TokenHelper.encode(payload={"user_id": str(user.id)}),
            refresh_token=TokenHelper.encode(payload={"sub": "refresh"}),
            token_type="bearer"
        )

    def is_admin(self, user_id: str) -> bool:
        user = self.user_repository.get_by_id(user_id)
        if not user:
            raise exceptions.user.UserNotFoundException()
        return getattr(user, "is_admin", False)

    def delete_user(self, user_id: str) -> None:
        try:
            user = self.user_repository.get_by_id(user_id)
            if not user:
                raise exceptions.user.UserNotFoundException()

            self.user_repository.delete(user)

            self.db_session.commit()  # Commit transaction after deletion
        except Exception as e:
            self.db_session.rollback()
            raise e

    def logout(self) -> None:
        raise NotImplementedError("Logout functionality is not implemented yet.")
