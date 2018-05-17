"""
API Server initialization.
"""
from flask import (Flask)
from werkzeug.contrib.fixers import (ProxyFix)
from config import (CONFIG_MAPPER)

def create_app(config_name='development'):
    """ Create the application with the relevant configuration. """
    app = Flask(__name__)
    app.config.from_object(CONFIG_MAPPER[config_name])
    app.wsgi_app = ProxyFix(app.wsgi_app)

    from . import extensions
    from . import modules
    for content in (
            extensions,
            modules,
    ):
        content.init_app(app)

    return app
