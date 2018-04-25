"""
Declares the server entity and its schema to allow for de/serialization to and from the database.
"""
from marshmallow import Schema, fields
from sqlalchemy import Column, String

from .entity import Entity, BASE


class Server(Entity, BASE):  # pylint: disable=too-few-public-methods
    """
    The server entity.
    """
    __tablename__ = 'servers'

    server_id = Column(String)
    server_name = Column(String)
    server_address = Column(String)
    server_port = Column(String)

    def __init__(self, server_id, server_name, server_address, server_port):
        Entity.__init__(self)
        self.server_id = server_id
        self.server_name = server_name
        self.server_address = server_address
        self.server_port = server_port


class ServerSchema(Schema):
    """
    The server schema.
    """
    id = fields.Number()
    server_id = fields.Str()
    server_name = fields.Str()
    server_address = fields.Str()
    server_port = fields.Str()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()
