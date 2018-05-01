"""
Defines the users end point. A user is a registered account linked with
one or more server IDs
"""
from flask import (
    jsonify
)

import json

from flask_restplus import (
    Resource,
)

from flask_cors import (
    cross_origin,
)

from api.authentication.authentication import (
    requires_auth,
    get_user_id,
)

from api.database.entities.entity import (
    SESSION,
    ENGINE,
    BASE
)

from api.database.entities.model import (
    User,
    UserSchema
)

from api.endpoints.users import NAMESPACE

BASE.metadata.create_all(ENGINE)


@NAMESPACE.route('/')
class UserList(Resource):
    '''Shows a list of all users and lets you POST to add new users'''
    @NAMESPACE.doc('list_users')
    @cross_origin(headers=["Content-Type", "Authorization"])
    @cross_origin(headers=["Access-Control-Allow-Origin", "*"])
    @requires_auth
    @NAMESPACE.doc(security='apikey')
    def get(self):
        '''Get the current users.'''
        session = SESSION()
        users_objects = session.query(User).all()

        # transforming into JSON-serializable objects
        schema = UserSchema(many=True)
        all_users = schema.dump(users_objects)

        # serializing as JSON
        session.close()
        return jsonify(all_users.data)

    @NAMESPACE.doc('create_user')
    @cross_origin(headers=["Content-Type", "Authorization"])
    @cross_origin(headers=["Access-Control-Allow-Origin", "*"])
    @requires_auth
    @NAMESPACE.doc(security='apikey')
    def post(self):
        ''' Post a new user. '''
        user_id = {
            "user_id" : get_user_id()
        }
        user_id = json.dumps(user_id)
        posted_user = UserSchema(
            only=('user_id')).load(user_id)
        print(posted_user)
        user = User(**posted_user.data)

        # persist user
        session = SESSION()
        session.add(user)
        session.commit()

        # Return created user
        new_user = UserSchema().dump(user).data
        session.close()
        return jsonify(new_user)
