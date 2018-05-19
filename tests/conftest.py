import pytest

from app import create_app

@pytest.yield_fixture(scope='session')
def flask_app():
    app = create_app('testing')
    return app


@pytest.fixture(scope='session')
def flask_app_client(flask_app):
    return flask_app.test_client()
