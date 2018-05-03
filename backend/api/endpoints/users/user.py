"""
Defines the user endpoint. For fetching information for a specific user
"""

from flask import (jsonify)
from flask_restplus import (Resource)
from flask_cors import (cross_origin)
from sqlalchemy.orm import (exc)
from api.authentication.authentication import (requires_auth)
from api.database.entities.entity import (SESSION)
from api.database.entities.model import (
    User as UserDB,
    UserSchema,
)
from api.endpoints.users import NAMESPACE


@NAMESPACE.route('/<string:user_id>')
@NAMESPACE.response(404, 'User not found')
@NAMESPACE.param('user_id', 'The user identifier')
class User(Resource):
    '''Show a single user and lets you delete a single user'''
    @NAMESPACE.doc('get_user')
    @cross_origin(headers=["Content-Type", "Authorization"])
    @cross_origin(headers=["Access-Control-Allow-Origin", "*"])
    @requires_auth
    @NAMESPACE.doc(security='apikey')
    def get(self, user_id):
        '''Get a specific user.'''
        session = SESSION()
        try:
            users_objects = session.query(
                UserDB).filter_by(user_id=user_id).one()
        except exc.NoResultFound:
            return "", 404

        # transforming into JSON-serializable objects
        schema = UserSchema()
        all_users = schema.dump(users_objects)

        # serializing as JSON
        session.close()
        return jsonify(all_users.data)

    @NAMESPACE.doc('delete_user')
    @NAMESPACE.response(204, 'User deleted')
    @cross_origin(headers=["Content-Type", "Authorization"])
    @cross_origin(headers=["Access-Control-Allow-Origin", "*"])
    @requires_auth
    @NAMESPACE.doc(security='apikey')
    def delete(self, user_id):
        '''Delete a user given its identifier'''
        session = SESSION()
        user = session.query(UserDB).filter_by(user_id=user_id).one()
        session.delete(user)
        session.commit()

        session.close()

        return "", 204

    @cross_origin(headers=["Content-Type", "Authorization"])
    @cross_origin(headers=["Access-Control-Allow-Origin", "*"])
    @requires_auth
    @NAMESPACE.doc(security='apikey')
    def put(self, user_id):
        '''Update a user given its identifier'''
        return_string = "Update user: " + user_id
        return return_string
