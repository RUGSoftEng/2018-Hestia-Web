"""
Create the API from the underlying endpoints.
"""
from flask_restplus import Api
from api.endpoints.servers.servers import NAMESPACE as SERVERS_NAMESPACE
from api.endpoints.users.users import NAMESPACE as USERS_NAMESPACE

API = Api(
    version='1.0',
    title='Hestia Web API',
    description='The Hestia Web Api, handling routing to your controllers.',
)

API.add_namespace(SERVERS_NAMESPACE)
API.add_namespace(USERS_NAMESPACE)
