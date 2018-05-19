"""
Modules enable logical resource separation.
"""

from app.extensions.api import (API)

from . import (
    servers,
    users,
)

def init_app(app):
    """ Initialize application modules. """
    for content in (
            servers,
            users,
    ):
        content.init_api(API)
