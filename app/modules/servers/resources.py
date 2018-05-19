from flask_restplus import (
    Resource,
    Namespace,
)

NAMESPACE = Namespace('servers', "The central point for all your server (controller) needs.")

@NAMESPACE.route('/')
class Servers(Resource):
    """ GET all servers, POST a new server. """
    def get(self):
        """
        List of servers.
        Returns a list of servers starting from ``offset`` limited by ``limit``
        parameter.
        """
        return "Getting servers"

    def post(self):
        """
        Add a server to the list of servers.
        """
        return "Posting server"


@NAMESPACE.route('/<string:server_id>')
@NAMESPACE.param('server_id', 'The server identifier')
class Server(Resource):
    """ GET a server, DELETE a server, PUT (update) a server """
    def get(self, server_id):
        """
        Get a server.
        """
        return "Getting server"

    def delete(self, server_id):
        """
        Delete a server.
        """
        return "Deleting server"

    def put(self, server_id):
        """
        Update the information of a server.
        """
        return "Updating server"

@NAMESPACE.route('/<string:server_id>/request')
@NAMESPACE.param('server_id', 'The server identifier')
class ServerRequest(Resource):
    """
    POST a request to be forwarded to a server.
    """
    def post(self, server_id):
        """
        Forward a request to a server.
        """
        return "Forwarding request to server"
