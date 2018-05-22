"""
Defines the server database model
"""

from app.extensions import (DB)
from sqlalchemy import Column, String, ForeignKey
from app.modules.util import (url_safe_uuid)

class ServerModel(DB.Model):
    """
    Server database model
    """
    __tablename__ = 'servers'

    server_id = Column(String, primary_key=True)
    user_id = Column(String, ForeignKey('users.user_id'))
    server_name = Column(String)
    server_address = Column(String)
    server_port = Column(String)

    def __init__(self, user_id, server_name, server_address, server_port):
        self.server_id = url_safe_uuid()
        self.user_id = user_id
        self.server_name = server_name
        self.server_address = server_address
        self.server_port = server_port
        super(ServerModel, self).__init__()
