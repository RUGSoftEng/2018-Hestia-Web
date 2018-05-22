"""
Defines the endpoints allowing for access and manipulation of users.
"""
from flask_restplus import (
    Resource,
    Namespace,
)

from app.extensions import (DB)
from app.extensions.auth.authentication import (
    requires_auth,
    get_user_id,
)
from .schemas import (UserSchema)
from .models import (UserModel)

NAMESPACE = Namespace('users', "Manipulate users of the system.")

@NAMESPACE.route('/')
class Users(Resource):
    """ POST a new user. """
    @requires_auth
    @NAMESPACE.doc(security='apikey')
    def post(self):
        """
        List of users.
        Returns a list of users starting from ``offset`` limited by ``limit``
        parameter.
        """
        user_id = {
            'user_id': get_user_id()
        }
        schema = UserSchema().load(user_id)
        new_user = UserModel(**schema.data)
        DB.session.begin()
        DB.session.add(new_user)
        DB.session.commit()

        return UserSchema().dump(new_user).data
