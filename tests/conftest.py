"""
Setup fixtures for pytest.
"""
import pytest

from app import create_app

@pytest.yield_fixture(scope='session')
def flask_app():
    """ Create flask application for testing. """
    app = create_app('testing')
    return app


@pytest.fixture(scope='session')
#pylint: disable=redefined-outer-name
def flask_app_client(flask_app):
    """ Create flask client to test HTTP responses. """
    return flask_app.test_client()
