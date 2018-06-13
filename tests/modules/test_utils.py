"""
Test utility functions
"""
# Note that only one function is unit-testable.

import pytest

import app.modules.util as util


def test_uuid_not_constant():
    """
    Assert that the UUID function does not return a constant value.
    """
    assert(util.url_safe_uuid() != util.url_safe_uuid())
