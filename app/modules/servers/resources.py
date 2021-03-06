"""
Defines the endpoints allowing for access and manipulation of servers.
A server represents a remote Hestia controller.
"""

import ast
from flask_restplus import (
    Resource,
    Namespace,
    fields,
)
from sqlalchemy.orm import (exc)
from app.extensions import (
    DB,
    AUTHENTICATOR,
)
from app.modules.util import (
    route_request,
    ping,
)
from .schemas import (ServerSchema)
from .models import (ServerModel)
from ..presets.resources import (Preset)


NAMESPACE = Namespace(
    'servers', "The central point for all your server (controller) needs.")

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
    @AUTHENTICATOR.requires_auth
    @NAMESPACE.doc(security='apikey')
    def get(self):
        """
        Get the list of servers.
        A server is associated with a user denoted by an authentication JWT.
        """

        servers = DB.session.query(
            ServerModel).filter_by(user_id=AUTHENTICATOR.get_user_id())

        # transforming into JSON-serializable objects
        schema = ServerSchema(many=True)
        all_servers = schema.dump(servers).data
        return all_servers

    @NAMESPACE.expect(SERVER)
    @AUTHENTICATOR.requires_auth
    @NAMESPACE.doc(security='apikey')
    def post(self):
        """
        Add a server to the list of servers.
        A server is associated with a user denoted by an authentication JWT.
        """

        payload = NAMESPACE.apis[0].payload
        print(payload)
        payload['user_id'] = AUTHENTICATOR.get_user_id()
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
    @AUTHENTICATOR.requires_auth
    @NAMESPACE.doc(security='apikey')
    def get(self, server_id):
        """
        Get a server.
        The server is identified by its ``server_id``
        """

        # Attempt to retrieve the SINGLE entry in the database with the server_id given.
        # Error 404 if >1 or D.N.E
        try:
            server_object = DB.session.query(
                ServerModel).filter_by(
                    server_id=server_id,
                    user_id=AUTHENTICATOR.get_user_id()
                ).one()
        except exc.NoResultFound:
            return "", 404

        # transforming into JSON-serializable objects
        server = ServerSchema().dump(server_object).data

        return server

    @AUTHENTICATOR.requires_auth
    @NAMESPACE.doc(security='apikey')
    def delete(self, server_id):
        """
        Delete a server.
        The server is identified by its ``server_id``
        """

        try:
            server = DB.session.query(ServerModel).filter_by(
                server_id=server_id, user_id=AUTHENTICATOR.get_user_id()).one()
        except exc.NoResultFound:
            return "", 404

        DB.session.begin()
        DB.session.delete(server)
        DB.session.commit()

        return "", 204

    @NAMESPACE.expect(SERVER)
    @AUTHENTICATOR.requires_auth
    @NAMESPACE.doc(security='apikey')
    def put(self, server_id):
        """
        Update the information of a server.
        The server is identified by its ``server_id``. The data which may be
        updated is the ``server_name``, the ``server_address``, and the
        ``server_port``
        """
        DB.session.begin()
        try:
            server = DB.session.query(ServerModel).filter_by(
                server_id=server_id, user_id=AUTHENTICATOR.get_user_id()).one()
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


REQUEST_PAYLOAD = NAMESPACE.model('request_payload', {
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
class ServerRequest(Resource):
    """
    POST a request to a server.

    A request represents an abstract payload to be forwarded to another REST
    API. A request is composed of a ``request_type`` representing the rest
    verb, and ``endpoint`` representing the resource endpoint, and an
    ``optionalPayload`` representing an auxiliary JSON object required to
    perform the verb on the resource.
    """

    @NAMESPACE.expect(REQUEST_PAYLOAD)
    @AUTHENTICATOR.requires_auth
    @NAMESPACE.doc(security='apikey')
    def post(self, server_id):
        """
        Forward a request to a server.
        """

        try:
            server_object = DB.session.query(
                ServerModel).filter_by(
                    server_id=server_id,
                    user_id=AUTHENTICATOR.get_user_id()
                ).one()
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


@NAMESPACE.route('/<string:server_id>/ping')
@NAMESPACE.param('server_id', 'The server identifier')
class ServerPing(Resource):
    """
    POST request to get the ping associated with the server.
    """

    @AUTHENTICATOR.requires_auth
    @NAMESPACE.doc(security='apikey')
    def post(self, server_id):
        """
        Post a ping request to a server.
        """

        try:
            server_object = DB.session.query(
                ServerModel).filter_by(
                    server_id=server_id,
                    user_id=AUTHENTICATOR.get_user_id()
                ).one()
        except exc.NoResultFound:
            return "", 404

        # transforming into JSON-serializable objects
        server = ServerSchema().dump(server_object).data

        server_query = server['server_address'] + ':' + server['server_port']
        return ping(server_query)


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
    @AUTHENTICATOR.requires_auth
    @NAMESPACE.doc(security='apikey')
    def post(self, server_id):
        """
        Apply a preset (stored in a preset) whose contents are to be applied to a server.
        """

        try:
            server_object = DB.session.query(
                ServerModel).filter_by(
                    server_id=server_id,
                    user_id=AUTHENTICATOR.get_user_id()
                ).one()
        except exc.NoResultFound:
            return "", 404

        # transforming into JSON-serializable objects
        server = ServerSchema().dump(server_object).data
        server_url = server["server_address"] + ":" + server["server_port"]

        preset_id = NAMESPACE.apis[0].payload["preset_id"]
        preset_object = Preset().get(server_id, preset_id)
        preset = ast.literal_eval(preset_object["preset_state"])

        for device in preset:
            for activator in device["activators"]:
                query = (server_url +
                         f"/devices/{device['deviceId']}" +
                         f"/activators/{activator['activatorId']}")
                payload = {"state": activator["state"]}
                route_request("POST", query, payload)

        # transforming into JSON-serializable objects
        return "Batch request successful"
