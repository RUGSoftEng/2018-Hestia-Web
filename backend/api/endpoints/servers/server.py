from flask_restplus import (
    Resource,
    fields,
)
from api.endpoints.servers import NAMESPACE
SERVER = NAMESPACE.model('Server', {
    'server_id': fields.String(readOnly=True, description="The server identification"),
    'server_owner': fields.String(readOnly=True, description="Owner of the server"),
    'server_name': fields.String(readOnly=True, description="The server identification"),
    'server_address': fields.String(readOnly=True, description="The server identification"),
    'server_port': fields.String(readOnly=True, description="The server identification"),

})
