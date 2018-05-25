"""
Defines the endpoints allowing for access and manipulation of servers.
A server represents a remote Hestia controller.
"""

from flask_restplus import (
    Resource,
    Namespace,
    fields,
)
from sqlalchemy.orm import (exc) # TODO there may be a more elegant way to manage this
from app.extensions import (DB)
from app.modules.util import (route_request)
from app.extensions.auth.authentication import (
    requires_auth,
    get_user_id,
)
from .schemas import (ServerSchema)
from .models import (ServerModel)


NAMESPACE = Namespace('servers', "The central point for all your server (controller) needs.")

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

@NAMESPACE.route('/')
class Servers(Resource):
    """ GET all servers, POST a new server. """
    @requires_auth
    @NAMESPACE.doc(security='apikey')
    def get(self):
        """
        List of servers.
        Returns a list of servers starting from ``offset`` limited by ``limit``
        parameter.
        """

        servers = DB.session.query(
            ServerModel).filter_by(user_id=get_user_id())

        # transforming into JSON-serializable objects
        schema = ServerSchema(many=True)
        all_servers = schema.dump(servers).data
        return all_servers

    @NAMESPACE.expect(SERVER)
    @requires_auth
    @NAMESPACE.doc(security='apikey')
    def post(self):
        """
        Add a server to the list of servers.
        """

        payload = NAMESPACE.apis[0].payload
        payload['user_id'] = get_user_id()
        posted_server = ServerSchema(
            only=('user_id',
                  'server_name',
                  'server_address',
                  'server_port')).load(payload)

        server = ServerModel(**posted_server.data)

        # persist server
        DB.session.begin()
        DB.session.add(server)
        DB.session.commit()

        # return created server
        return ServerSchema().dump(server).data


@NAMESPACE.route('/<string:server_id>')
@NAMESPACE.param('server_id', 'The server identifier')
class Server(Resource):
    """ GET a server, DELETE a server, PUT (update) a server """
    @requires_auth
    @NAMESPACE.doc(security='apikey')
    def get(self, server_id):
        """
        Get a server.
        """

        # Attempt to retrieve the SINGLE entry in the database with the server_id given.
        # Error 404 if >1 or D.N.E
        try:
            server_object = DB.session.query(
                ServerModel).filter_by(server_id=server_id, user_id=get_user_id()).one()
        except exc.NoResultFound:
            return "", 404

        # transforming into JSON-serializable objects
        server = ServerSchema().dump(server_object).data

        return server

    @requires_auth
    @NAMESPACE.doc(security='apikey')
    def delete(self, server_id):
        """
        Delete a server.
        """

        try:
            server = DB.session.query(ServerModel).filter_by(
                server_id=server_id, user_id=get_user_id()).one()
        except exc.NoResultFound:
            return "", 404

        DB.session.begin()
        DB.session.delete(server)
        DB.session.commit()

        return "", 204

    @NAMESPACE.expect(SERVER)
    @requires_auth
    @NAMESPACE.doc(security='apikey')
    def put(self, server_id):
        """
        Update the information of a server.
        """
        DB.session.begin()
        try:
            server = DB.session.query(ServerModel).filter_by(
                server_id=server_id, user_id=get_user_id()).one()
        except exc.NoResultFound:
            return "", 404

        payload = NAMESPACE.apis[0].payload

        if "server_name" in payload:
            server.server_name = payload["server_name"]
        if "server_address" in payload:
            server.server_address = payload["server_address"]
        if "server_port" in payload:
            server.server_port = payload["server_port"]

        user_server = ServerSchema().dump(server).data

        DB.session.commit()
        DB.session.close()

        # serializing as JSON for return
        return user_server

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

@NAMESPACE.route('/<string:server_id>/ping')
@NAMESPACE.param('server_id', 'The server identifier')
class ServerRequest(Resource):
    """
    GET the ping associated with the server.
    """

    @requires_auth
    @NAMESPACE.doc(security='apikey')
    def post(self, server_id):
        """
        Forward a request to a server.
        """

        try:
            server_object = DB.session.query(
                ServerModel).filter_by(server_id=server_id, user_id=get_user_id()).one()
        except exc.NoResultFound:
            return "", 404

        # transforming into JSON-serializable objects
        server = ServerSchema().dump(server_object).data

        request_type = NAMESPACE.apis[0].payload["requestType"]
        endpoint = NAMESPACE.apis[0].payload["endpoint"]
        optional_payload = NAMESPACE.apis[0].payload["optionalPayload"]
        server_query = server['server_address'] + \
            ':' + server['server_port'] + endpoint
        return route_request(request_type, server_query, optional_payload)

@NAMESPACE.route('/<string:server_id>/request')
@NAMESPACE.param('server_id', 'The server identifier')
class ServerRequest(Resource):
    """
    POST a request to be forwarded to a server.
    """

    @NAMESPACE.expect(PAYLOAD)
    @requires_auth
    @NAMESPACE.doc(security='apikey')
    def post(self, server_id):
        """
        Forward a request to a server.
        """

        try:
            server_object = DB.session.query(
                ServerModel).filter_by(server_id=server_id, user_id=get_user_id()).one()
        except exc.NoResultFound:
            return "", 404

        # transforming into JSON-serializable objects
        server = ServerSchema().dump(server_object).data

        request_type = NAMESPACE.apis[0].payload["requestType"]
        endpoint = NAMESPACE.apis[0].payload["endpoint"]
        optional_payload = NAMESPACE.apis[0].payload["optionalPayload"]
        server_query = server['server_address'] + \
            ':' + server['server_port'] + endpoint
        return ping(server['server_address'] + ":" + server['server_port'])


BATCH_PAYLOAD = NAMESPACE.model('batch_payload', {
    'preset_id': fields.String(
        readOnly=True,
        description='The type of request to make to the server'
    ),
})

@NAMESPACE.route('/<string:server_id>/batch_request')
@NAMESPACE.param('server_id', 'The server identifier')
class ServerBatchRequest(Resource):
    """
    POST a batch request (stored in a preset) whose contents are to be applied to a server.
    """

    @NAMESPACE.expect(BATCH_PAYLOAD)
    @requires_auth
    @NAMESPACE.doc(security='apikey')
    def post(self, server_id):
        """
        Apply a preset (stored in a preset) whose contents are to be applied to a server.
        """

        try:
            server_object = DB.session.query(
                ServerModel).filter_by(server_id=server_id, user_id=get_user_id()).one()
        except exc.NoResultFound:
            return "", 404

        # transforming into JSON-serializable objects
        server = ServerSchema().dump(server_object).data

        request_type = NAMESPACE.apis[0].payload["requestType"]
        endpoint = NAMESPACE.apis[0].payload["endpoint"]
        optional_payload = NAMESPACE.apis[0].payload["optionalPayload"]
        server_query = server['server_address'] + \
            ':' + server['server_port'] + endpoint
        return ping(server['server_address'] + ":" + server['server_port'])
