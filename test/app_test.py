import os
import tempfile
from typing import Any, Generator
from flask import Flask
import pytest
from app.app import create_app
from app.database import init_db


@pytest.fixture
def test_app() -> Generator[Flask, None, None]:
    settings = os.getenv('APP_TESTING_SETTINGS_MODULE')
    db_fd, db_path = tempfile.mkstemp()

    app = create_app(settings)

    with app.app_context():
        init_db()

    yield app

    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def client(app: Flask) -> Any:
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()
