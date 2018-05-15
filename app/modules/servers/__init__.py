"""
Servers module
"""

from flask import (Blueprint)
from app.modules.api import (API)

from flask_restplus import (Namespace)

NAMESPACE = Namespace('servers', description='All servers of the system')

def init_app(app):
    """
    Init servers module.
    """

    # # Touch underlying modules
    from . import (
                   resources,
    )

    API.add_namespace(NAMESPACE)
