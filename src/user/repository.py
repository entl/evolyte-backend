from sqlalchemy.orm import Session

from src.repository import BaseRepository
from .models import User


class UserRepository(BaseRepository[User]):
    def __init__(self, db: Session):
        super().__init__(User, db)
