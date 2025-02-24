from typing import Optional, List
from .schemas import UserOut, UserCreate, UserUpdate, LoginResponse
from .models import User

from src.core.exceptions.user import UserNotFoundException, PasswordDoesNotMatchException
from src.core.exceptions.user import DuplicateEmailOrUsernameException

from src.core.utils import password_helper
from src.core.utils.token_helper import TokenHelper
from src.core.db.uow import UnitOfWork


class UserService:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    def get_all_users(self) -> List[UserOut]:
        users = self.uow.users.get_all()
        return [UserOut.model_validate(user) for user in users]

    def get_user_by_id(self, user_id: int) -> Optional[UserOut]:
        user = self.uow.users.get_by(id=user_id)
        return UserOut.model_validate(user) if user else None

    def get_user_by_username(self, username: str) -> Optional[UserOut]:
        user = self.uow.users.get_by(username=username)
        return UserOut.model_validate(user) if user else None

    def get_user_by_email(self, email: str) -> Optional[UserOut]:
        user = self.uow.users.get_by(email=email)
        return UserOut.model_validate(user) if user else None

    def create_user(self, user: UserCreate) -> UserOut:
        with self.uow:
            # Check for duplicate username or email
            if self.uow.users.get_by(username=user.username):
                raise DuplicateEmailOrUsernameException()
            if self.uow.users.get_by(email=user.email):
                raise DuplicateEmailOrUsernameException()

            # Hash the password before storing
            hashed_password = password_helper.hash(user.password)
            user.password = hashed_password

            new_user = User(**user.model_dump())
            created_user = self.uow.users.create(new_user)

            return UserOut.model_validate(created_user)

    def update_user(self, user_update: UserUpdate) -> UserOut:
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

            return UserOut.model_validate(updated_user)

    def login(self, email: str, password: str) -> LoginResponse:
        user = self.uow.users.get_by(email=email)
        if not user:
            raise UserNotFoundException()
        if not password_helper.verify(password, user.password):
            raise PasswordDoesNotMatchException()

        return LoginResponse(
            access_token=TokenHelper.encode(payload={"user_id": str(user.id)}),
            refresh_token=TokenHelper.encode(payload={"sub": "refresh"}),
            token_type="bearer"
        )

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
