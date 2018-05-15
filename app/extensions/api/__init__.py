"""
API extension.
"""

from flask_restplus import (
    Api,
    Namespace,
    Resource,
)

API = Api(
    version='1.0',
    title='Hestia Web API',
    description='The Hestia Web Api, handling routing to your controllers.',
)
