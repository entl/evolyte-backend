from typing import Optional, List, Type
from sqlalchemy.orm import Session
from .models import User


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, user_id: int) -> Optional[User]:
        return self.db.query(User).filter(User.id == user_id).first()

    def get_by_username(self, username: str) -> Optional[User]:
        return self.db.query(User).filter(User.username == username).first()

    def get_by_email(self, email: str) -> Optional[User]:
        return self.db.query(User).filter(User.email == email).first()

    def get_all(self) -> List[User]:
        return self.db.query(User).all()

    def create(self, user: User) -> User:

        self.db.add(user)
        self.db.flush()  # Ensure ID is generated
        self.db.refresh(user)  # Refresh to load any DB-generated values
        return user

    def update(self, user: User) -> User:

        self.db.flush()  # Ensure changes are pushed to the database
        self.db.refresh(user)  # Refresh after flush
        return user

    def delete(self, user: User) -> None:
        self.db.delete(user)
