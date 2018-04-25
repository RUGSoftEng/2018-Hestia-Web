"""
Setup the API namespace for servers
"""
from flask_restplus import Namespace

NAMESPACE = Namespace(
    'servers', description='All servers (controllers) of the system')
