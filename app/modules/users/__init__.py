""" Intializations"""
from app.extensions.api import (API)

from flask_restplus import Namespace

NAMESPACE = Namespace(
    'servers', description='All servers (controllers) of the system')

def init_app(app):
    """
    Init servers module.
    """
    API.add_namespace(NAMESPACE)

    # # Touch underlying modules
    # from . import (models,
    #                resources,
    # )

    # API.add_namespace(resources.api)
