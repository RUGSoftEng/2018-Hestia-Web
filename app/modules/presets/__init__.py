"""
Presets module
"""

def init_api(api):
    """
    Init presets module.
    """

    ## Touch underlying resources
    from . import (resources)

    api.add_namespace(resources.NAMESPACE)
