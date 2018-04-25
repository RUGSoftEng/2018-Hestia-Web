"""
Declares the user entity and its schema to allow for de/serialization to and from the database.
"""
from marshmallow import Schema, fields
from sqlalchemy import Table, Column, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

from .entity import Entity, BASE


class User(Entity, BASE):  # pylint: disable=too-few-public-methods
    """
    The user entity.
    """
    __tablename__ = 'users'

    user_id = Column(String, primary_key=True)
    server_ids = relationship("Server")

    def __init__(self, user_id, server_idss):
        Entity.__init__(self)
        self.user_id = user_id
        self.server_idss = server_idss


class UserSchema(Schema):
    """
    The users schema.
    """
    user_id = fields.Str()
    server_ids = fields.Integer()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()
