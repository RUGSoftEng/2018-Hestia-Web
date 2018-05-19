"""
Defines the endpoints allowing for access and manipulation of users.
"""

from flask_restplus import (
    Resource,
    Namespace,
)

NAMESPACE = Namespace('users', "Manipulate users of the system.")

@NAMESPACE.route('/')
class Users(Resource):
    """ POST a new user. """
    def post(self):
        """
        List of users.
        Returns a list of users starting from ``offset`` limited by ``limit``
        parameter.
        """
        return "Posting user"
