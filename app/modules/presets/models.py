"""
Defines the preset database model
"""

from sqlalchemy import (
    Column,
    String,
    ForeignKey,
    Integer,
)
from sqlalchemy.dialects.postgresql import *
from app.extensions import (DB)
from app.modules.util import (url_safe_uuid)

class PresetModel(DB.Model):
    """
    Preset database model
    """
    __tablename__ = 'presets'

    preset_id = Column(Integer, primary_key=True, autoincrement=True)
    server_id = Column(String, ForeignKey('servers.server_id'))
    preset_name = Column(String)
    preset_state = Column(String)
