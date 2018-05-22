"""
Defines the user database model
"""
from sqlalchemy import (
    Column,
    String,
)
from sqlalchemy.orm import (relationship)
from app.extensions import (DB)

class UserModel(DB.Model):
    """
    User database model
    """
    __tablename__ = 'users'

    user_id = Column(String, primary_key=True)
    servers = relationship("ServerModel", cascade="all, delete-orphan")
