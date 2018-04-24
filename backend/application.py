from flask import Flask, jsonify, json, request
from flask_restplus import Api, Resource, fields, reqparse
from .entities.entity import Session, engine, Base
from .entities.servers import Server, ServerSchema
from bson.objectid import ObjectId
from werkzeug.contrib.fixers import ProxyFix
import requests

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)
api = Api(app, version='1.0', title='Hestia Web API',
          description='The central web API, handling the routing of requests to local Hestia controllers',
)

Base.metadata.create_all(engine)

ns = api.namespace('servers', description='Server operations')

server = ns.model('Server', {
    'serverID': fields.String(readOnly=True, description="The server identification"),
    'serverName': fields.String(readOnly=True, description="The server identification"), 
    'serverAddress': fields.String(readOnly=True, description="The server identification"),
    'serverPort': fields.String(readOnly=True, description="The server identification"),

})

@ns.route('/')
class ServerList(Resource):
    '''Shows a list of all servers, and lets you POST to add new servers'''
    @ns.doc('list_servers')
    def get(self):
        '''List all servers'''
        session = Session()
        servers_objects = session.query(Server).all()

        # transforming into JSON-serializable objects
        schema = ServerSchema(many=True)
        all_servers = schema.dump(servers_objects)

        # serializing as JSON
        session.close()
        return jsonify(all_servers.data)

    @ns.expect(server)
    @ns.doc('create_server')
    def post(self):
        # mount exam object
        posted_server = ServerSchema(only=('serverID', 'serverName', 'serverAddress', 'serverPort'))\
                                           .load(api.payload)

        blah_server = Server(**posted_server.data, created_by="HTTP post request")

        # persist exam
        session = Session()
        session.add(blah_server)
        session.commit()

        # return created exam
        new_server = ServerSchema().dump(blah_server).data
        session.close()
        return jsonify(new_server)

if __name__ == '__main__':
    app.run(debug=True)
