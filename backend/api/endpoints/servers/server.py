from flask_restplus import (
    Resource,
    fields,
)
from api.endpoints.servers import NAMESPACE
SERVER = NAMESPACE.model('Server', {
    'server_id': fields.String(
        readOnly=True,
        description="The server identification"
    ),
    'server_owner': fields.String(
        readOnly=True,
        description="Owner of the server"
    ),
    'server_name': fields.String(
        readOnly=True,
        description="The server identification"
    ),
    'server_address': fields.String(
        readOnly=True,
        description="The server identification"
    ),
    'server_port': fields.String(
        readOnly=True,
        description="The server identification"
    ),
})

@NAMESPACE.route('/<string:id>')
@NAMESPACE.response(404, 'Server not found')
@NAMESPACE.param('id', 'The server identifier')
class Server(Resource):
    '''Show a single server item and lets you delete it'''
    @NAMESPACE.doc('get_server')
    @NAMESPACE.marshal_with(SERVER)
    def get(self, id):
        '''Fetch a given resource'''
        return "get"

    @NAMESPACE.doc('delete_server')
    @NAMESPACE.response(204, 'Server deleted')
    def delete(self, id):
        '''Delete a server given its identifier'''
        return "delete"
        return '', 204

    @NAMESPACE.expect(SERVER)
    @NAMESPACE.marshal_with(SERVER)
    def put(self, id):
        '''Update a server given its identifier'''
        return "request"


payload = NAMESPACE.model("raw_payload", {
    "required_info": fields.Raw(
        attribute="required_info",
        required=False,
        description="The information to be forwarded to the server.",
    )
})


PAYLOAD = NAMESPACE.model('payload', {
    'requestType': fields.String(
        readOnly=True,
        description='The type of request to make to the server'
    ),
    'endpoint': fields.String(
        readOnly=True,
        description='The endpoint on the remote server to interact with'
    ),
    'optionalPayload': fields.Raw(
        readOnly=True,
        required=False,
        description='The information to be forwarded to the remote server.'
    ),
})

@NAMESPACE.route('/<string:id>/request')
@NAMESPACE.param('id', 'The server identifier')
@NAMESPACE.expect(PAYLOAD)
class ServerRequest(Resource):
    @NAMESPACE.doc('request_from_server')
    def post(self, id):
        '''Forward a request to a server'''
        # server = DAO.get(id)
        # requestType = api.payload["requestType"]
        # endpoint = api.payload["endpoint"]
        # optionalPayload = api.payload["optionalPayload"]
        # return routeRequest(requestType, server['IPAddress']+':'+ server['port'] + endpoint, optionalPayload)
        return "Forward request"
