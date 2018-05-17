from flask_restplus import (
    Resource,
    Namespace,
)

NAMESPACE = Namespace('users', "Manipulate users of the system.")

@NAMESPACE.route('/')
class Users(Resource):
    """ GET all servers, POST a new server. """
    def post(self):
        """
        List of servers.
        Returns a list of users starting from ``offset`` limited by ``limit``
        parameter.
        """
        return "Hello"
