from flask import Flask, jsonify, json, request
from flask_restplus import Api, Resource, fields, reqparse
from bson.objectid import ObjectId
from werkzeug.contrib.fixers import ProxyFix
import requests

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)
api = Api(app, version='1.0', title='Hestia Web API',
          description='The central web API, handling the routing of requests to local Hestia controllers',
)

ns = api.namespace('servers', description='Server operations')

server = ns.model('Server', {
    'id': fields.String(readOnly=True, description='The server unique identifier'),
    'IPAddress': fields.String(readOnly=True, description='The remote servers IP Address'),
    'port': fields.String(readOnly=True, description='The remote servers port'),
})

class ServerDAO(object):
    def __init__(self):
        self.counter = 0
        self.servers = []

    def get(self, id):
        for server in self.servers:
            if server['id'] == id:
                return server
        api.abort(404, "Server {} doesn't exist".format(id))

    def create(self, data):
        server = data
        server['id'] = str(ObjectId())
        self.servers.append(server)
        return server

    def update(self, id, data):
        server = self.get(id)
        server.update(data)
        return server

    def delete(self, id):
        server = self.get(id)
        self.servers.remove(server)


DAO = ServerDAO()
DAO.create({'IPAddress': 'http://0.0.0.0',
            'port': '8000',
}
)


@ns.route('/')
class ServerList(Resource):
    '''Shows a list of all servers, and lets you POST to add new servers'''
    @ns.doc('list_servers')
    @ns.marshal_list_with(server)
    def get(self):
        '''List all servers'''
        return DAO.servers

    @ns.doc('create_server')
    @ns.expect(server)
    @ns.marshal_with(server, code=201)
    def post(self):
        '''Create a new server'''
        return DAO.create(api.payload), 201


@ns.route('/<string:id>')
@ns.response(404, 'Server not found')
@ns.param('id', 'The server identifier')
class Server(Resource):
    '''Show a single server item and lets you delete it'''
    @ns.doc('get_server')
    @ns.marshal_with(server)
    def get(self, id):
        '''Fetch a given resource'''
        return DAO.get(id)

    @ns.doc('delete_server')
    @ns.response(204, 'Server deleted')
    def delete(self, id):
        '''Delete a server given its identifier'''
        DAO.delete(id)
        return '', 204

    @ns.expect(server)
    @ns.marshal_with(server)
    def put(self, id):
        '''Update a server given its identifier'''
        return DAO.update(id, api.payload)


payload = ns.model("raw_payload", {
    "required_info": fields.Raw(attribute="required_info", required=False,
                                   description="The information to be forwarded to the server.")
})


payload = ns.model('payload', {
    'requestType': fields.String(readOnly=True, description='The type of request to make to the server'),
    'endpoint': fields.String(readOnly=True, description='The endpoint on the remote server to interact with'),
    'optionalPayload': fields.Raw(readOnly=True, required=False, description='The information to be forwarded to the remote server.'),
})

@ns.route('/<string:id>/request')
@ns.param('id', 'The server identifier')
@ns.expect(payload)
class ServerRequest(Resource):
    @ns.doc('request_from_server')
    def post(self, id):
        '''Forward a request to a server'''
        server = DAO.get(id)
        requestType = api.payload["requestType"]
        endpoint = api.payload["endpoint"]
        optionalPayload = api.payload["optionalPayload"]
        return routeRequest(requestType, server['IPAddress']+':'+ server['port'] + endpoint, optionalPayload)

TIMEOUT = 1.0
def routeRequest(method, query, payload):
    result = ""
    method = method.upper()
    print("Sending request to server:", method, ", ", query, ", ", payload)
    if (method == "GET"):
        result = requests.get(query, verify=False, timeout=TIMEOUT).json()
    elif (method == "POST"):
        result = requests.post(query, verify=False, json=payload, timeout=TIMEOUT).json()
    elif (method == "PUT"):
        result = requests.put(query, verify=False, json=payload, timeout=TIMEOUT).json()
    elif (method == "DELETE"):
        result = requests.delete(query, verify=False, timeout=TIMEOUT)
    else:
        result = "Invalid REST method."
    return result

if __name__ == '__main__':
    app.run(debug=True)
