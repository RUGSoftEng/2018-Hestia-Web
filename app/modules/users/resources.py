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

    @requires_auth
    @NAMESPACE.doc(security='apikey')
    def delete(self):
        """
        Delete a user.
        A user is identified by its ``user_id`` from the authentication JWT.
        """

        try:
            user = DB.session.query(UserModel).filter_by(user_id=get_user_id()).one()
        except exc.NoResultFound:
            return "", 404

        DB.session.begin()
        DB.session.delete(user)
        DB.session.commit()

        return "", 204
