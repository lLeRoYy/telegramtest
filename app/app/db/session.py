import asyncio
from contextvars import ContextVar
from abc import ABC, abstractmethod

# sync
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine

# async
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import (
    async_sessionmaker,
    create_async_engine,
    async_scoped_session,
)

scope: ContextVar = ContextVar("db_session_scope")


def scopefunc():
    try:
        return scope.get()
    except LookupError:
        print("scope not set")


class ABCSession(ABC):
    @abstractmethod
    def __init__(self, db_url: str) -> None:
        raise NotImplementedError

    @abstractmethod
    def create_session(self):
        raise NotImplementedError


class SyncSession(ABCSession):
    def __init__(self, db_url: str):
        self.engine = create_engine(url=str(db_url))
        self.session_factory = sessionmaker(bind=self.engine)
        self.Session = scoped_session(self.session_factory)

    def create_session(self):
        return self.Session()


class ASyncSession(ABCSession):

    def __init__(self, db_url: str) -> None:
        self.engine = create_async_engine(str(db_url))
        self.session_factory = async_sessionmaker(self.engine, expire_on_commit=False)
        self.session = async_scoped_session(self.session_factory, asyncio.current_task)

    def create_session(self) -> AsyncSession:
        return self.session()
