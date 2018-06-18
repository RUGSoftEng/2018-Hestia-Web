"""
Users module
"""

def init_api(api):
    """
    Init users module.
    """

    ## Touch underlying resources
    from . import (resources)

    api.add_namespace(resources.NAMESPACE)
