"""
Servers module
"""

from app.extensions.api import (API)

def init_app(app):
    """
    Init servers module.
    """

    ## Touch underlying modules
    from . import (
        resources,
    )

    API.add_namespace(resources.NAMESPACE)
