from abc import ABC
from contextvars import ContextVar

from sqlalchemy.orm import DeclarativeBase, sessionmaker, Session
from sqlalchemy import create_engine

from src.settings import settings

# Context variable for session tracking
session_context: ContextVar[str] = ContextVar("session_context")


def get_session_context() -> str:
    return session_context.get()


# Define the synchronous database URL
SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.pg_database_username}:{settings.pg_database_password}" \
                          f"@{settings.pg_database_hostname}/{settings.pg_database_name}"

# Create a synchronous SQLAlchemy engine
engine = create_engine(SQLALCHEMY_DATABASE_URL, future=True)

# Create a session factory
SessionFactory = sessionmaker(bind=engine, autoflush=False, autocommit=False)

Base = DeclarativeBase()


# Unit of Work Pattern
class UnitOfWorkBase(ABC):
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        raise NotImplementedError()

    def commit(self):
        raise NotImplementedError()

    def rollback(self):
        raise NotImplementedError()

    def close(self):
        raise NotImplementedError()

    def refresh(self, entity):
        raise NotImplementedError()


class UnitOfWork(UnitOfWorkBase):
    def __init__(self, session: Session):
        self.session = session

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            print("Rolling back transaction", exc_type, exc_val, exc_tb)
            self.session.rollback()
        else:
            print("Committing transaction")
            self.session.commit()
        self.session.close()

    def commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()

    def close(self):
        self.session.close()

    def refresh(self, entity: DeclarativeBase):
        self.session.refresh(entity)
