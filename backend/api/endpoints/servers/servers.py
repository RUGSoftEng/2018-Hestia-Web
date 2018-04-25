"""
Defines the servers end point. A server represents a remote Hestia controller.
"""
from flask import (
    jsonify
)

from flask_restplus import (
    Resource,
    fields,
)

from api.database.entities.entity import (
    SESSION,
    ENGINE,
    BASE
)

from api.database.entities.servers import (
    Server,
    ServerSchema
)

from api.endpoints.servers import NAMESPACE

BASE.metadata.create_all(ENGINE)

SERVER = NAMESPACE.model('Server', {
    'server_id': fields.String(readOnly=True, description="The server identification"),
    'server_name': fields.String(readOnly=True, description="The server identification"),
    'server_address': fields.String(readOnly=True, description="The server identification"),
    'server_port': fields.String(readOnly=True, description="The server identification"),

})


@NAMESPACE.route('/')
class ServerList(Resource):
    '''Shows a list of all servers, and lets you POST to add new servers'''
    @NAMESPACE.doc('list_servers')
    def get(self): # pylint: disable=no-self-use
        '''Get the current servers.'''
        session = SESSION()
        servers_objects = session.query(Server).all()

        print(servers_objects)
        # transforming into JSON-serializable objects
        schema = ServerSchema(many=True)
        all_servers = schema.dump(servers_objects)

        # serializing as JSON
        session.close()
        return jsonify(all_servers.data)

    @NAMESPACE.expect(SERVER)
    @NAMESPACE.doc('create_server')
    def post(self): # pylint: disable=no-self-use
        '''Post a new server.'''
        # mount exam object
        posted_server = ServerSchema(
            only=('server_id',
                  'server_name',
                  'server_address',
                  'server_port')).load(NAMESPACE.apis[0].payload)

        server = Server(**posted_server.data)

        # persist exam
        session = SESSION()
        session.add(server)
        session.commit()

        # return created exam
        new_server = ServerSchema().dump(server).data
        session.close()
        return jsonify(new_server)
