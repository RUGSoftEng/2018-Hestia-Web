"""
API extension.
"""

from flask_restplus import (
    Api,
    Namespace,
    Resource,
)

from flask import (Blueprint)
AUTHORIZATIONS = {
    'apikey': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'authorization'
    }
}

API_BLUEPRINT = Blueprint('api', __name__)
API = Api(
    API_BLUEPRINT,
    version='1.0',
    title='Hestia Web API',
    description='The Hestia Web Api, handling routing to your controllers.',
    authorizations=AUTHORIZATIONS,

)

def init_app(app):
    """ Initializes the app at entry point. """
    app.register_blueprint(API_BLUEPRINT)
