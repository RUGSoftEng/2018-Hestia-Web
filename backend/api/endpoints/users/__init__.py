"""
Setup the API namespace for servers
"""
from flask_restplus import Namespace

NAMESPACE = Namespace('users', description='All users of the system')
