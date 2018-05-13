"""
Defines the servers end point. A server represents a remote Hestia controller.
"""
from flask import (jsonify)
from flask_cors import (cross_origin)
from flask_restplus import (Resource)
from api.authentication.authentication import (
    requires_auth,
    get_user_id,
)
from api.database.entities.entity import (
    SESSION,
    ENGINE,
    BASE,
)
from api.database.entities.model import (
    Server,
    ServerSchema,
)
from api.endpoints.servers import (NAMESPACE)
from api.endpoints.servers.server import (SERVER)


BASE.metadata.create_all(ENGINE)

@NAMESPACE.route('/')
class ServerList(Resource):
    '''Shows a list of all servers, and lets you POST to add new servers'''
    @NAMESPACE.doc('list_servers')
    @cross_origin(headers=["Content-Type", "Authorization"])
    @cross_origin(headers=["Access-Control-Allow-Origin", "*"])
    @requires_auth
    @NAMESPACE.doc(security='apikey')
    def get(self):
        '''Get the current servers.'''
        session = SESSION()
        servers_objects = session.query(
            Server).filter_by(user_id=get_user_id())

        # transforming into JSON-serializable objects
        schema = ServerSchema(many=True)
        all_servers = schema.dump(servers_objects)

        # serializing as JSON
        session.close()
        return jsonify(all_servers.data)

    @NAMESPACE.expect(SERVER)
    @NAMESPACE.doc('create_server')
    @cross_origin(headers=["Content-Type", "Authorization"])
    @cross_origin(headers=["Access-Control-Allow-Origin", "*"])
    @requires_auth
    @NAMESPACE.doc(security='apikey')
    def post(self):
        '''Post a new server.'''
        payload = NAMESPACE.apis[0].payload
        payload['user_id'] = get_user_id()
        posted_server = ServerSchema(
            only=('user_id',
                  'server_name',
                  'server_address',
                  'server_port')).load(payload)

        server = Server(**posted_server.data)

        # persist server
        session = SESSION()
        session.add(server)
        session.commit()

        # return created server
        new_server = ServerSchema().dump(server).data
        session.close()
        return jsonify(new_server)
