"""
Declare the model objects for the database as well as schema for each
"""
import uuid
import base64
from marshmallow import Schema, fields
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship

from .entity import Entity, BASE


class User(Entity, BASE):
    """
    The user entity.
    """
    __tablename__ = 'users'

    user_id = Column(String, primary_key=True)
    servers = relationship("Server", cascade="all, delete-orphan")

    def __init__(self, user_id):
        Entity.__init__(self)
        self.user_id = user_id


class UserSchema(Schema):
    """
    The users schema.
    """
    user_id = fields.Str()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()


class Server(Entity, BASE):
    """
    The server entity.
    """
    __tablename__ = 'servers'

    server_id = Column(String, primary_key=True)
    user_id = Column(String, ForeignKey('users.user_id'))
    server_name = Column(String)
    server_address = Column(String)
    server_port = Column(String)

    def __init__(self, user_id, server_name, server_address, server_port):
        Entity.__init__(self)
        self.server_id = (str(base64.urlsafe_b64encode(uuid.uuid4().bytes))).replace("=", "").replace("\'","")[1:]
        self.user_id = user_id
        self.server_name = server_name
        self.server_address = server_address
        self.server_port = server_port


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
