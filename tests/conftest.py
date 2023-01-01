"""Test configurations/"""
from pathlib import Path
from typing import Iterator

import pytest
from sqlalchemy.orm import Session

from todocli import Config
from todocli.base import get_session


@pytest.fixture(scope='session', name='session')
def get_db_session() -> Iterator[Session]:
    """Create app instance as fixture.

    :yield: app
    :rtype: Iterator[App]
    """

    config = Config('sqlite:///todo-test.sqlite')

    yield get_session(config)

    db_file_path = Path(
        Path(__file__).resolve().parent.parent, 'todo-test.sqlite')
    if db_file_path.is_file():
        db_file_path.unlink()
