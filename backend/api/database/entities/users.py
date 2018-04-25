"""
Declares the user entity and its schema to allow for de/serialization to and from the database.
"""
from marshmallow import Schema, fields
from sqlalchemy import Column, String

from .entity import Entity, BASE


class User(Entity, BASE):  # pylint: disable=too-few-public-methods
    """
    The user entity.
    """
    __tablename__ = 'users'

    user_id = Column(String)
    servers_id = Column(String)

    def __init__(self, user_id, servers_id):
        Entity.__init__(self)
        self.user_id = user_id
        self.servers_id = servers_id


class UserSchema(Schema):
    """
    The users schema.
    """
    id = fields.Number()
    user_id = fields.Str()
    servers_id = fields.Str()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()
