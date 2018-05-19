"""
Testing utils
-------------
"""

from contextlib import contextmanager
from datetime import datetime, timedelta
import json

from flask import Response
from flask.testing import FlaskClient
from werkzeug.utils import cached_property


class AutoAuthFlaskClient(FlaskClient):
    """
    A helper FlaskClient class with a useful for testing ``login`` context
    manager.
    """

    def __init__(self, *args, **kwargs):
        super(AutoAuthFlaskClient, self).__init__(*args, **kwargs)

    def open(self, *args, **kwargs):
        response = super(AutoAuthFlaskClient, self).open(*args, **kwargs)

        return response


class JSONResponse(Response):
    # pylint: disable=too-many-ancestors
    """
    A Response class with extra useful helpers, i.e. ``.json`` property.
    """

    @cached_property
    def json(self):
        return json.loads(self.get_data(as_text=True))


def generate_user_instance(
        user_id=None,
        username="username",
        password=None,
        email=None,
        first_name="First Name",
        middle_name="Middle Name",
        last_name="Last Name",
        created=None,
        updated=None,
        is_active=True,
        is_regular_user=True,
        is_admin=False,
        is_internal=False
):
    """
    Returns:
        user_instance (User) - an not committed to DB instance of a User model.
    """
    # pylint: disable=too-many-arguments
    from app.modules.users.models import User
    if password is None:
        password = '%s_password' % username
    user_instance = User(
        id=user_id,
        username=username,
        first_name=first_name,
        middle_name=middle_name,
        last_name=last_name,
        password=password,
        email=email or '%s@email.com' % username,
        created=created or datetime.now(),
        updated=updated or datetime.now(),
        is_active=is_active,
        is_regular_user=is_regular_user,
        is_admin=is_admin,
        is_internal=is_internal
    )
    user_instance.password_secret = password
return user_instance
