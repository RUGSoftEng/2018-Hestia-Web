"""
Defines the preset database model
"""

from sqlalchemy import (
    Column,
    String,
    ForeignKey,
)
from app.extensions import (DB)
from app.modules.util import (url_safe_uuid)

class PresetModel(DB.Model):
    """
    Preset database model
    """
    __tablename__ = 'presets'

    preset_id = Column(String, primary_key=True)
    server_id = Column(String, ForeignKey('servers.server_id'))
    preset_name = Column(String)

    def __init__(self, server_id, preset_name):
        self.preset_id = url_safe_uuid()
        self.server_id = server_id
        self.preset_name = preset_name
        super(PresetModel, self).__init__()
