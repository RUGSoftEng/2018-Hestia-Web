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
        Returns a list of users starting from ``offset`` limited by ``limit``
        parameter.
        """
        return "Hello"
