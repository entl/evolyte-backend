from sqlalchemy.orm import Session

from src.repository import BaseRepository

from .models import Identity


class IdentityRepository(BaseRepository[Identity]):
    def __init__(self, db: Session):
        super().__init__(Identity, db)
