"""
Extensions allows for access to common resources throughout the application.
"""

from flask_cors import (CORS)
from flask_marshmallow import (Marshmallow)
from app.extensions.auth.authentication import (Authenticator)
from .flask_sqlalchemy import (SQLAlchemy)

CROSS_ORIGIN_RESOURCE_SHARING = CORS()
MARSHMALLOW = Marshmallow()
DB = SQLAlchemy()
AUTHENTICATOR = Authenticator()

def init_app(app):
    """ Initialize application extensions. """
    from . import api
    for extension in (
            api,
            CROSS_ORIGIN_RESOURCE_SHARING,
            DB,
            MARSHMALLOW,
            AUTHENTICATOR
    ):
        extension.init_app(app)
