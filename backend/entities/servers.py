# coding=utf-8
from marshmallow import Schema, fields
from sqlalchemy import Column, String

from .entity import Entity, Base


class Server(Entity, Base):
    __tablename__ = 'servers'

    serverID = Column(String)
    serverName = Column(String)
    serverAddress = Column(String)
    serverPort = Column(String)

    def __init__(self, serverID, serverName, serverAddress, serverPort, created_by):
        Entity.__init__(self, created_by)
        self.serverID = serverID
        self.serverName = serverName
        self.serverAddress = serverAddress
        self.serverPort = serverPort

class ServerSchema(Schema):
    id = fields.Number()
    serverID = fields.Str()
    serverName = fields.Str()
    serverAddress = fields.Str()
    serverPort = fields.Str()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()
    last_updated_by = fields.Str()
