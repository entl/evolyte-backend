from contextvars import ContextVar

from sqlalchemy.orm import DeclarativeBase, sessionmaker
from sqlalchemy import create_engine

from src.settings import settings

# Context variable for session tracking
session_context: ContextVar[str] = ContextVar("session_context")


def get_session_context() -> str:
    return session_context.get()


# Define the synchronous database URL
SQLALCHEMY_DATABASE_URL = (
    f"postgresql://{settings.pg_database_username}:{settings.pg_database_password}"
    f"@{settings.pg_database_hostname}/{settings.pg_database_name}"
)

# Create a synchronous SQLAlchemy engine
engine = create_engine(SQLALCHEMY_DATABASE_URL, future=True)

# Create a session factory
SessionFactory = sessionmaker(bind=engine, autoflush=False, autocommit=False)


class Base(DeclarativeBase):
    pass
