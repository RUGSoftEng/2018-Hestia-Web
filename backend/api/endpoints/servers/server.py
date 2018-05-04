"""
Creates endpoints for the individual server access
"""
import requests
from flask import (jsonify)
from flask_restplus import (
    Resource,
    fields,
)
from flask_cors import (cross_origin)
from sqlalchemy.orm import (exc)
from api.authentication.authentication import (
    requires_auth,
    get_user_id,
)
from api.database.entities.entity import (SESSION)
from api.database.entities.model import (
    Server as ServerDB,
    ServerSchema,
)
from api.endpoints.servers import NAMESPACE

SERVER = NAMESPACE.model('Server', {
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


@NAMESPACE.route('/<string:server_id>')
@NAMESPACE.response(404, 'Server not found')
@NAMESPACE.param('server_id', 'The server identifier')
class Server(Resource):
    '''Show a single server item and lets you delete it'''
    @NAMESPACE.doc('get_server')
    @cross_origin(headers=["Content-Type", "Authorization"])
    @cross_origin(headers=["Access-Control-Allow-Origin", "*"])
    @requires_auth
    @NAMESPACE.doc(security='apikey')
    def get(self, server_id):
        '''Get a specific server.'''
        session = SESSION()

        # Attempt to retrieve the SINGLE entry in the database with the server_id given.
        # Error 404 if >1 or D.N.E
        try:
            server_object = session.query(
                ServerDB).filter_by(server_id=server_id, user_id=get_user_id()).one()
        except exc.NoResultFound:
            return "", 404

        # transforming into JSON-serializable objects
        schema = ServerSchema()
        user_server = schema.dump(server_object).data

        # serializing as JSON for return
        session.close()
        return jsonify(user_server)

    @NAMESPACE.doc('delete_server')
    @NAMESPACE.response(204, 'Server deleted')
    @cross_origin(headers=["Content-Type", "Authorization"])
    @cross_origin(headers=["Access-Control-Allow-Origin", "*"])
    @requires_auth
    @NAMESPACE.doc(security='apikey')
    def delete(self, server_id):
        '''Delete a server given its identifier'''
        session = SESSION()
        try:
            server = session.query(ServerDB).filter_by(
                server_id=server_id, user_id=get_user_id()).one()
        except exc.NoResultFound:
            return "", 404

        session.delete(server)
        session.commit()

        session.close()

        return "", 204

    @NAMESPACE.expect(SERVER)
    @NAMESPACE.marshal_with(SERVER)
    @cross_origin(headers=["Content-Type", "Authorization"])
    @cross_origin(headers=["Access-Control-Allow-Origin", "*"])
    @requires_auth
    @NAMESPACE.doc(security='apikey')
    def put(self, server_id):
        '''Update a server given its identifier'''
        return_string = "Update server: " + server_id
        return return_string


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


@NAMESPACE.route('/<string:server_id>/request')
@NAMESPACE.param('server_id', 'The server identifier')
@NAMESPACE.expect(PAYLOAD)
class ServerRequest(Resource):
    """
    Defines the request class that sends a request to a controller
    """
    @NAMESPACE.doc('request_from_server')
    @cross_origin(headers=["Content-Type", "Authorization"])
    @cross_origin(headers=["Access-Control-Allow-Origin", "*"])
    @requires_auth
    @NAMESPACE.doc(security='apikey')
    def post(self, server_id):
        '''Forward a request to a server'''
        session = SESSION()
        try:
            server_object = session.query(
                ServerDB).filter_by(server_id=server_id, user_id=get_user_id()).one()
        except exc.NoResultFound:
            return "", 404

        # transforming into JSON-serializable objects
        schema = ServerSchema()
        server = schema.dump(server_object).data

        request_type = NAMESPACE.apis[0].payload["requestType"]
        endpoint = NAMESPACE.apis[0].payload["endpoint"]
        optional_payload = NAMESPACE.apis[0].payload["optionalPayload"]
        server_query = server['server_address'] + \
            ':' + server['server_port'] + endpoint
        return route_request(request_type, server_query, optional_payload)


TIMEOUT = 1.0


def route_request(method, query, payload):
    """
    Defines the route function to send commands to a controller
    """
    result = ""
    method = method.upper()
    print("Sending request to server:", method, ", ", query, ", ", payload)
    if method == "GET":
        result = requests.get(query, verify=False, timeout=TIMEOUT).json()
    elif method == "POST":
        result = requests.post(query, verify=False,
                               json=payload, timeout=TIMEOUT).json()
    elif method == "PUT":
        result = requests.put(query, verify=False,
                              json=payload, timeout=TIMEOUT).json()
    elif method == "DELETE":
        result = requests.delete(query, verify=False, timeout=TIMEOUT)
    else:
        result = "Invalid REST method."
    return jsonify(result)
