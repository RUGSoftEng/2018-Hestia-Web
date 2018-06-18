"""
Modules enable logical resource separation.
"""

from app.extensions.api import (API)
from app.extensions import (DB)

from . import (
    servers,
    users,
    presets,
)

def init_app(app):
    """ Initialize application modules. """
    for content in (
            servers,
            users,
            presets,
    ):
        content.init_api(API)
