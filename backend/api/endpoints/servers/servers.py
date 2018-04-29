"""
Defines the servers end point. A server represents a remote Hestia controller.
"""
from flask import (
    jsonify
)

from flask_restplus import (
    Resource,
)

from api.database.entities.entity import (
    SESSION,
    ENGINE,
    BASE
)

from api.database.entities.model import (
    Server,
    ServerSchema,
)

from api.endpoints.servers import NAMESPACE

from api.endpoints.servers.server import SERVER

BASE.metadata.create_all(ENGINE)


@NAMESPACE.route('/')
@requires_auth
class ServerList(Resource):
    '''Shows a list of all servers, and lets you POST to add new servers'''
    @NAMESPACE.doc('list_servers')
    def get(self):
        '''Get the current servers.'''
        session = SESSION()
        servers_objects = session.query(Server).all()

        # transforming into JSON-serializable objects
        schema = ServerSchema(many=True)
        all_servers = schema.dump(servers_objects)

        # serializing as JSON
        session.close()
        return jsonify(all_servers.data)

    @NAMESPACE.expect(SERVER)
    @NAMESPACE.doc('create_server')
    def post(self):
        '''Post a new server.'''
        posted_server = ServerSchema(
            only=('server_id',
                  'user_id',
                  'server_name',
                  'server_address',
                  'server_port')).load(NAMESPACE.apis[0].payload)

        server = Server(**posted_server.data)

        # persist server
        session = SESSION()
        session.add(server)
        session.commit()

        # return created server
        new_server = ServerSchema().dump(server).data
        session.close()
        return jsonify(new_server)
