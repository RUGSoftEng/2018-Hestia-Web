"""
Declare the model objects for the database as well as schema for each
"""
from marshmallow import Schema, fields

class UserSchema(Schema):
    """
    The users schema.
    """
    user_id = fields.Str()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()
