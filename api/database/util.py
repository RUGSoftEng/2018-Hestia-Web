"""
Utility functions for database
"""

import base64
import uuid

def url_safe_uuid():
    '''
    Returns a url safe uuid.
    '''
    return str(base64.urlsafe_b64encode(uuid.uuid4().bytes)).replace("=", "").replace("\'", "")[1:]
