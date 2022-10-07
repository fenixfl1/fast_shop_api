import os
import tempfile
from typing import Any, Generator
from flask import Flask
import pytest
from app.app import create_app
from app.database import init_db
import json


@pytest.fixture()
def app() -> Generator[Flask, None, None]:
    settings = os.getenv('APP_TESTING_SETTINGS_MODULE')
    db_fd, db_path = tempfile.mkstemp()

    app = create_app(settings)

    with app.app_context():
        init_db()

    yield app

    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture()
def client(app: Flask) -> Any:
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()


class AuthActions(object):

    def __init__(self, client):
        self._client = client

    def create_user(self, user_data):
        return self._client.post(
            '/api/v1.0.0/register_user',
            data=json.dumps(user_data),
            headers={"Content-Type": "application/json"}
        )

    def login(self, username='test', password='test'):
        data = {
            'USERNAME': username,
            'PASSWORD': password
        }
        return self._client.post(
            '/api/v1.0.0/login',
            data=json.dumps(data),
            headers={"Content-Type": "application/json"}
        )

    def logout(self):
        return self._client.get('/auth/logout')


def test_create_user(client):
    auth = AuthActions(client)

    resp = auth.create_user({
        "EMAIL": "test@user.com",
        "FIRST_NAME": "test",
        "LAST_NAME": "test",
        "PASSWORD": "test",
        "USERNAME": "test",
        "STATE": "A"
    })

    assert resp.status_code == 200
    assert resp.json


def test_auth(client):
    auth = AuthActions(client)
    result = auth.login(username='admin', password='admin')

    assert result.status_code == 200
    assert result.json['message'] == 'Wellcome test test'
