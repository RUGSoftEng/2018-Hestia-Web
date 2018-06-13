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

from app.modules.servers.schemas import (ServerSchema)
from app.modules.servers.models import (ServerModel)


@pytest.yield_fixture(scope='session')
def flask_app():
    """ Create base flask application for testing. """
    app = create_app('testing')
    app.app_context().push()
    DB.drop_all(app=app)
    DB.create_all(app=app)
    return app


@pytest.yield_fixture(scope='session')
def flask_app_user_in_db():
    """ Create flask application for testing with a user in the DB. """
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


@pytest.yield_fixture(scope='session')
def flask_app_server_in_db():
    """ Create flask application with user and a server in the DB. """
    app = flask_app_user_in_db()
    payload = {
        'user_id':'1',
        'server_name': 'string',
        'server_address': 'string',
        'server_port': 'string'
    }
    posted_server = ServerSchema(
        only=('user_id',
              'server_name',
              'server_address',
              'server_port')).load(payload)
    server = ServerModel(**posted_server.data)

    DB.session.begin()
    DB.session.add(server)
    DB.session.commit()
    return app


@pytest.fixture(scope='session')
#pylint: disable=redefined-outer-name
def flask_app_authenticated_client(flask_app):
    """ Create an authentaicated flask client to test HTTP responses. """
    AUTHENTICATOR.set_user_id("1")
    return flask_app.test_client()


@pytest.fixture(scope='session')
#pylint: disable=redefined-outer-name
def flask_app_authenticated_client_in_DB(flask_app_user_in_db):
    """ Create an authenticated flask client with that same user in the DB. """
    AUTHENTICATOR.set_user_id("1")

    return flask_app_user_in_db.test_client()

@pytest.fixture(scope='session')
#pylint: disable=redefined-outer-name
def flask_app_authenticated_client_in_DB_with_server(flask_app_server_in_db):
    """ Create an authenticated flask client with that user and server in the DB. """
    AUTHENTICATOR.set_user_id("1")

    return flask_app_server_in_db.test_client()

@pytest.fixture(scope='session')
#pylint: disable=redefined-outer-name
def flask_app_client(flask_app):
    """ Create flask client to test HTTP responses. """
    return flask_app.test_client()
