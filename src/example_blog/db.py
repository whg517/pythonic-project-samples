"""Database connections"""
import functools
import logging
from typing import Callable

from sqlalchemy import event
from sqlalchemy.engine import create_engine
from sqlalchemy.engine.base import Engine
from sqlalchemy.engine.url import URL
from sqlalchemy.orm import scoped_session, sessionmaker

from example_blog.config import settings

url = URL(
    drivername=settings.DATABASE.DRIVER,
    username=settings.DATABASE.USERNAME,
    password=settings.DATABASE.PASSWORD,
    host=settings.DATABASE.HOST,
    port=settings.DATABASE.PORT,
    database=settings.DATABASE.DATABASE,
    query=settings.DATABASE.QUERY,
)

engine: Engine = create_engine(url, echo=False)

SessionFactory = sessionmaker(bind=engine, autocommit=False, autoflush=True)

ScopedSession = scoped_session(SessionFactory)


@event.listens_for(Engine, "connect")
def set_sqlite_pragma(db_api_connection, connection_record):
    """SQLite Foreign key support
    https://docs.sqlalchemy.org/en/14/dialects/sqlite.html?highlight=pragma#foreign-key-support
    """
    from sqlite3 import Connection

    if isinstance(db_api_connection, Connection):
        cursor = db_api_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()


def injection_session(func: Callable):
    """Injection session to callable.
    This decorator not support async. So it executor blocking code.
    eg:
    """
    @functools.wraps(func)
    def __wrapper(*args, **kwargs):
        ScopedSession()
        logging.debug(ScopedSession.registry.registry.value)
        # Injection session
        kwargs.setdefault('session', ScopedSession)
        try:
            return func(*args, **kwargs)
        finally:
            ScopedSession.remove()

    return __wrapper
