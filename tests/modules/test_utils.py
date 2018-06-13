import pytest

import app.modules.util as util


def test_uuid_not_constant():
    assert(util.url_safe_uuid() != util.url_safe_uuid())
