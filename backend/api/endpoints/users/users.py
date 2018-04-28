"""
Defines the users end point. A user is a registered account linked with
one or more server IDs
"""
from flask import (
    jsonify
)

from flask_restplus import (
    Resource,
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

from api.endpoints.users.user import USER

BASE.metadata.create_all(ENGINE)


@NAMESPACE.route('/')
class UserList(Resource):
    '''Shows a list of all users and lets you POST to add new users'''
    @NAMESPACE.doc('list_users')
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

    @NAMESPACE.expect(USER)
    @NAMESPACE.doc('create_user')
    def post(self):
        ''' Post a new user. '''
        posted_user = UserSchema(
            only=('user_id',
                  'servers_id')).load(NAMESPACE.apis[0].payload)

        user = User(**posted_user.data)

        # persist user
        session = SESSION()
        session.add(user)
        session.commit()

        # Return created user
        new_user = UserSchema().dump(user).data
        session.close()
        return jsonify(new_user)
