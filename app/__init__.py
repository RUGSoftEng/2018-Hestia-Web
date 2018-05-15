"""
API Server initialization.
"""
from flask import (Flask)
from flask_sqlalchemy import (SQLAlchemy)
from werkzeug.contrib.fixers import (ProxyFix)
from config import (CONFIG_MAPPER)
import app.extensions as extensions
import app.modules as modules

DB = SQLAlchemy()

def create_app(config_name='development'):
    """ Create the application with the relevant configuration. """
    app = Flask(__name__)
    app.config.from_object(CONFIG_MAPPER[config_name])
    app.wsgi_app = ProxyFix(app.wsgi_app)
    for content in (
            extensions,
            modules,
    ):
        content.init_app(app)

    return app
