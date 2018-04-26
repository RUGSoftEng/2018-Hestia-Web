from flask_restplus import (
    Resource,
    fields,
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
    @NAMESPACE.marshal_with(USER)
    def get(self, id):
        '''Fetch a given resource'''
        return "get"

    @NAMESPACE.doc('delete_user')
    @NAMESPACE.response(204, 'User deleted')
    def delete(self, id):
        '''Delete a user given its identifier'''
        return "delete"
        return '', 204

    @NAMESPACE.expect(USER)
    @NAMESPACE.marshal_with(USER)
    def put(self, id):
        '''Update a user given its identifier'''
        return "request"
