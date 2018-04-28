"""
Defines the user endpoint. For fetching information for a specific user
"""

from flask import (
    jsonify
)

from flask_restplus import (
    Resource,
    fields,
)

from sqlalchemy.orm import (exc)

from api.database.entities.entity import(
    SESSION,
)

from api.database.entities.model import(
    User as UserDB,
    UserSchema,
)

from api.endpoints.users import NAMESPACE

USER = NAMESPACE.model('User', {
    'user_id': fields.String(readOnly=True, description="The user identification"),
    'server_ids': fields.String(readOnly=True, description="The server that the user is tied to"),

})

@NAMESPACE.route('/<string:id>')
@NAMESPACE.response(404, 'User not found')
@NAMESPACE.param('id', 'The user identifier')
class User(Resource):
    '''Show a single user and lets you delete a single user'''
    @NAMESPACE.doc('get_user')
    def get(self, id):
        '''Get a specific user.'''
        session = SESSION()
        try:
            users_objects = session.query(UserDB).filter_by(user_id=id).one()
        except exc.NoResultFound as e:
            return "", 404

        # transforming into JSON-serializable objects
        schema = UserSchema()
        all_users = schema.dump(users_objects)

        # serializing as JSON
        session.close()
        return jsonify(all_users.data)


    @NAMESPACE.doc('delete_user')
    @NAMESPACE.response(204, 'User deleted')
    def delete(self, id):
        '''Delete a user given its identifier'''
        session = SESSION()
        user = session.query(UserDB).filter_by(user_id=id).one()
        session.delete(user)
        session.commit()

        session.close()

        return "", 204

    @NAMESPACE.expect(USER)
    @NAMESPACE.marshal_with(USER)
    def put(self, id):
        '''Update a user given its identifier'''
        returnString = "Update user: " + id
        return "return /user/put"
