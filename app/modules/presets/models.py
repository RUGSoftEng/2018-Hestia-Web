"""
Defines the preset database model
"""

from sqlalchemy import (
    Column,
    String,
    ForeignKey,
    Integer,
)

from app.extensions import (DB)

class PresetModel(DB.Model):
    """
    Preset database model
    """
    __tablename__ = 'presets'

    preset_id = Column(Integer, primary_key=True, autoincrement=True)
    server_id = Column(String, ForeignKey('servers.server_id'))
    preset_name = Column(String)
    preset_state = Column(String)
