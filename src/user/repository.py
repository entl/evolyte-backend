from typing import Optional, List
from sqlalchemy.orm import Session
from .models import User
from ..repository import BaseRepository


class UserRepository(BaseRepository[User]):
    def __init__(self, db: Session):
        super().__init__(User, db)
