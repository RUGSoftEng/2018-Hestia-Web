# coding=utf-8
from marshmallow import Schema, fields
from sqlalchemy import Column, String

from .entity import Entity, BASE

class User(Entity, BASE): # pylint: disable=too-few-public-methods
    """
    The user entity.
    """
    __tablename__ = 'users'

    userID = Column(String)
    serversID = Column(String)

    def __init__(self, userID, serversID, created_by):
        Entity.__init__(self, created_by)
        self.userID = userID
        self.serversID = serversID

class UserSchema(Schema):
    """
    The users schema.
    """
    id = fields.Number()
    userID = fields.Str()
    serversID = fields.Str()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()
    last_updated_by = fields.Str()