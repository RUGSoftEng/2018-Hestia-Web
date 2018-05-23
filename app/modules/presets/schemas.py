"""
Declare the model objects for the database as well as schema for each
"""
from marshmallow import Schema, fields

class PresetSchema(Schema):
    """
    The preset schema.
    """
    preset_id = fields.Str()
    server_id = fields.Str()
    preset_name = fields.Str()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()
