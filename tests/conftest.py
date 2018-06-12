"""
Setup fixtures for pytest.
"""
import pytest

from app import (create_app)
from app.extensions import (
    DB,
    AUTHENTICATOR,
)

from app.modules.users.schemas import (UserSchema)
from app.modules.users.models import (UserModel)

@pytest.yield_fixture(scope='session')
def flask_app():
    """ Create flask application for testing. """
    app = create_app('testing')
    DB.drop_all(app=app)
    DB.create_all(app=app)
    return app

@pytest.yield_fixture(scope='session')
def flask_app_user_in_db():
    """ Create flask application for testing. """
    app = create_app('testing')
    DB.drop_all(app=app)
    DB.create_all(app=app)
    app.app_context().push()

    user_id = {
        'user_id': "1"
    }

    schema = UserSchema().load(user_id)
    new_user = UserModel(**schema.data)
    DB.session.begin()
    DB.session.add(new_user)
    DB.session.commit()
    return app

@pytest.fixture(scope='session')
#pylint: disable=redefined-outer-name
def flask_app_authenticated_client(flask_app):
    """ Create flask client to test HTTP responses. """
    AUTHENTICATOR.set_user_id("1")
    return flask_app.test_client()

@pytest.fixture(scope='session')
#pylint: disable=redefined-outer-name
def flask_app_authenticated_client_in_DB(flask_app_user_in_db):
    """ Create flask client to test HTTP responses. """
    AUTHENTICATOR.set_user_id("1")

    return flask_app_user_in_db.test_client()

@pytest.fixture(scope='session')
#pylint: disable=redefined-outer-name
def flask_app_client(flask_app):
    """ Create flask client to test HTTP responses. """
    return flask_app.test_client()
