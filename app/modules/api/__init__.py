"""
Flask-RESTplus API registration module
"""

from flask import (Blueprint)
from app.extensions.api import (API)

def init_app(app):
    """ Initializes the API """
    api_v1_blueprint = Blueprint('api', __name__)
    API.init_app(api_v1_blueprint)
    app.register_blueprint(api_v1_blueprint)
