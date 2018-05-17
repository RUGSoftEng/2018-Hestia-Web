"""
Users module
"""

from app.extensions.api import (API)

def init_app(app):
    """
    Init users module.
    """

    # # Touch underlying modules
    from . import (
        resources,
    )

    API.add_namespace(resources.NAMESPACE)
