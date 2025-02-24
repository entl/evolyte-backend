from typing import Type, TypeVar, Generic, Optional, List
from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.declarative import DeclarativeMeta

T = TypeVar("T", bound=DeclarativeMeta)


class BaseRepository(Generic[T]):
    # Generic repository that works with any SQLAlchemy model.
    def __init__(self, model: Type[T], session: Session):
        self.session = session
        self.model = model

    def get_by(self, **filters) -> Optional[T]:
        try:
            return self.session.query(self.model).filter_by(**filters).first()
        except NoResultFound:
            return None

    def get_all(self) -> List[T]:
        return self.session.query(self.model).all()

    def create(self, obj_data: T) -> T:
        self.session.add(obj_data)
        self.session.flush()
        self.session.refresh(obj_data)
        return obj_data

    def update(self, obj_data: T) -> T:
        self.session.flush()
        self.session.refresh(obj_data)
        return obj_data

    def delete(self, obj_data: T) -> None:
        self.session.delete(obj_data)
