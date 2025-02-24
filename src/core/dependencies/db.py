from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from src.core.db.session import SessionFactory
from src.core.db.uow import UnitOfWork


def get_db_session():
    return SessionFactory()


DBSessionDep = Annotated[Session, Depends(get_db_session)]


def get_uow(session: DBSessionDep):
    return UnitOfWork(session)


UowDep = Annotated[UnitOfWork, Depends(get_uow)]
