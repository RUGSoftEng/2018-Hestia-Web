"""
Defines the users end point. A user is a registered account linked with
one or more server IDs
"""
from flask import (
    jsonify
)

from flask_restplus import (
    Resource,
    fields,
)

from api.database.entities.entity import (
    SESSION,
    ENGINE,
    BASE
)

from api.database.entities.users import (
    User,
    UserSchema
)

from api.endpoints.servers import NAMESPACE

BASE.metadata.create_all(ENGINE)

USER = NAMESPACE.model('User',{
    'userID': fields.String(readOnly=True, description="The user"),
    'serversID': fields.String(readOnly=True, description="The server that the user is tied to"),

})

@NAMESPACE.route('/')
class UserList(Resource):
    '''Shows a list of all users and lets you POST to add new users'''
    @NAMESPACE.doc('list_users')
    def get(self): #pylint: disable=no-self-use
        '''Get the current users.'''
        session = SESSION()
        users_objects = session.query(User).all()

        print(users_objects)
        # transforming into JSON-serializable objects
        schema = UserSchema(many=True)
        all_users = schema.dump(users_objects)

        # serializing as JSON
        session.close()
        return jsonify(all_users.data)
    
    @NAMESPACE.expect(USER)
    @NAMESPACE.doc('create_user')
    def post(self): # pylint: disable=no-self-use
        ''' Post a new user. '''
        print(NAMESPACE.apis[1].payload)

        posted_user = UserSchema(
            only=('userID',
                  'serversID')).load(NAMESPACE.apis[0].payload)

        user = User(**posted_user.data)

        # persist user
        session = SESSION()
        session.add(user)
        session.commit()
        

        # Return created user
        new_user = UserSchema().dump(user).data
        session.close()
        return jsonify(new_user)