from flask_restplus import (
    Resource,
    fields,
)
from api.endpoints.users import NAMESPACE

USER = NAMESPACE.model('User', {
    'user_id': fields.String(readOnly=True, description="The user identification"),
    'server_ids': fields.String(readOnly=True, description="The server that the user is tied to"),

})
