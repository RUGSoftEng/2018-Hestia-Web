"""
Defines the user database model
"""


from app.extensions import (DB)
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship

class UserModel(DB.Model):
    """
    User database model
    """
    __tablename__ = 'users'

    user_id = Column(String, primary_key=True)
    servers = relationship("ServerModel", cascade="all, delete-orphan")

