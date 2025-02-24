from abc import ABC, abstractmethod

from sqlalchemy.orm import Session

from sqlalchemy.ext.declarative import DeclarativeMeta
from typing import TypeVar

from src.solar_panels.repository import SolarPanelRepository
from src.user.repository import UserRepository

# Generic type for database models
T = TypeVar("T", bound=DeclarativeMeta)


class UnitOfWorkBase(ABC):
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        raise NotImplementedError()

    @abstractmethod
    def commit(self):
        raise NotImplementedError()

    @abstractmethod
    def rollback(self):
        raise NotImplementedError()

    @abstractmethod
    def close(self):
        raise NotImplementedError()

    @abstractmethod
    def refresh(self, entity: T):
        raise NotImplementedError()


class UnitOfWork(UnitOfWorkBase):
    def __init__(self, session: Session):
        self.session = session
        self._user_repo = None
        self._solar_panel_repo = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            if exc_type:
                self.rollback()
            else:
                self.commit()
        finally:
            self.close()

    def commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()

    def close(self):
        self.session.close()

    def flush(self):
        self.session.flush()

    def refresh(self, entity: T):
        self.session.refresh(entity)

    def expunge(self, entity: T):
        self.session.expunge(entity)

    # lazy loading of repositories
    @property
    def users(self):
        if self._user_repo is None:
            self._user_repo = UserRepository(self.session)
        return self._user_repo

    @property
    def solar_panels(self):
        if self._solar_panel_repo is None:
            self._solar_panel_repo = SolarPanelRepository(self.session)
        return self._solar_panel_repo
