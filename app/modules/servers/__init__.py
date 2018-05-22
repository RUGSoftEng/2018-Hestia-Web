"""
Servers module
"""

def init_api(api):
    """
    Init servers module.
    """

    ## Touch underlying resources
    from . import (resources)

    api.add_namespace(resources.NAMESPACE)
