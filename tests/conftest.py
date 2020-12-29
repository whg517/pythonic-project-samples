"""Test config"""

import os
from pathlib import Path

import pytest
from alembic import command, config
from click.testing import CliRunner
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from example_blog import migration, server
from example_blog.config import settings
from example_blog.db import SessionFactory
from example_blog.models import Article


@pytest.fixture
def client():
    """Fast api test client factory"""
    _s = server.Server()
    _s.init_app()
    _c = TestClient(app=_s.app)
    yield _c


@pytest.fixture
def cli():
    runner = CliRunner(echo_stdin=True, mix_stderr=False)
    yield runner


@pytest.fixture()
def migrate():
    """Re-init database when run a test."""
    os.chdir(Path(migration.__file__).parent)
    alembic_config = config.Config('./alembic.ini')
    alembic_config.set_main_option('script_location', os.getcwd())
    print('\n----- RUN ALEMBIC MIGRATION, DB URI: \n')
    command.downgrade(alembic_config, 'base')
    command.upgrade(alembic_config, 'head')
    try:
        yield
    finally:
        command.downgrade(alembic_config, 'base')
        db_name = settings.DATABASE.get('NAME')
        if settings.DATABASE.DRIVER == 'sqlite' and os.path.isfile(db_name):
            try:
                os.remove(db_name)
            except FileNotFoundError:
                pass


@pytest.fixture()
def session(migrate) -> Session:
    """session fixture"""
    _s = SessionFactory()
    yield _s
    _s.close()


@pytest.fixture()
def init_article(session):
    """Init article"""
    a_1 = Article(title='Hello world', body='Hello world, can you see me?')
    a_2 = Article(title='Love baby', body='I love you everyday, and i want with you.')
    a_3 = Article(title='Tomorrow', body='When the sun rises, this day is fine day, cheer up.')
    session.add_all([a_1, a_2, a_3])
    session.commit()
