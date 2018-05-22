"""
Defines the endpoints allowing for access and manipulation of users.
"""
from flask_restplus import (
    Resource,
    Namespace,
)

from app.extensions import (DB)
from .schemas import (UserSchema)
from .models import (UserModel)
from app.modules.util import (commit_or_abort)

NAMESPACE = Namespace('users', "Manipulate users of the system.")

def get_user_id():
    return "1"

@NAMESPACE.route('/')
class Users(Resource):
    """ POST a new user. """
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
