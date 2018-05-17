"""
API extension.
"""

from flask_restplus import (
    Api,
    Namespace,
    Resource,
)

from flask import (Blueprint)

api_blueprint = Blueprint('api', __name__)
API = Api(
    api_blueprint,
    version='1.0',
    title='Hestia Web API',
    description='The Hestia Web Api, handling routing to your controllers.',
)

def init_app(app):
    """ Initializes the app at entry point. """
    app.register_blueprint(api_blueprint)
