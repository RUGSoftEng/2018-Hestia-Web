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
    api.init_app(app)
    servers.init_app(app)
    users.init_app(app)
