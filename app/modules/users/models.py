"""
Defines the user database model
"""

from app.extensions import (DB)

class User(DB.Model):
    """
    User database model
    """
    __tablename__ = 'users'

    user_id = Column(String, primary_key=True)
    servers = relationship("Server", cascade="all, delete-orphan")

    def __init__(self, user_id):
        Entity.__init__(self)
        self.user_id = user_id
