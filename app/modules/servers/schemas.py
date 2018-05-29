"""
Declare the model objects for the database as well as schema for each
"""
from marshmallow import Schema, fields

class ServerSchema(Schema):
    """
    The server schema.
    """
    server_id = fields.Str()
    user_id = fields.Str()
    server_name = fields.Str()
    server_address = fields.Str()
    server_port = fields.Str()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()
