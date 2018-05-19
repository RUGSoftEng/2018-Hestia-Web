"""
Modules enable logical resource separation.
"""

from . import (
    api,
    servers,
    users,
)

def init_app(app):
    """ Initialize application modules. """
    for content in (
            api,
            servers,
            users,
    ):
        content.init_app(app)
