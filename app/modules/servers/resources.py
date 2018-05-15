from flask_restplus import (
    Resource,
)
from . import (NAMESPACE)


@NAMESPACE.route('/')
class Users(Resource):
    """ Manipulations with users. """
    def get(self, args):
        """
        List of users.
        Returns a list of users starting from ``offset`` limited by ``limit``
        parameter.
        """
        return "Hello"
