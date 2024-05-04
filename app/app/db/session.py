from contextvars import ContextVar
from functools import wraps

from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine
from app.db.base import Base

scope: ContextVar = ContextVar('db_session_scope')


def scopefunc():
    try:
        return scope.get()
    except LookupError:
        print("scope not set")


class SyncSession:

    def __init__(self, db_url: str, dispose_session: bool = False):
        self.db_url = db_url
        self.dispose_session = dispose_session
        self.sync_engine = create_engine(str(self.db_url), pool_pre_ping=True, echo=True)
        self.sync_session_factory = sessionmaker(bind=self.sync_engine, autoflush=False, expire_on_commit=False)
        self.scoped_session = scoped_session(self.sync_session_factory, scopefunc=scopefunc)
        self.session = self.scoped_session()

    def create_database(self):
        Base.metadata.create_all(bind=self.sync_engine)


def commit_and_close_session(func):
    """Декоратор для комита и закрытия сессии"""

    @wraps(func)
    def session_manager(*args, **kwargs):
        session = SyncSession()
        try:
            result = func(session, *args, **kwargs)
            session.commit()
            return result
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
    return session_manager
