"""
Test server endpoints.
"""
import pytest


@pytest.mark.parametrize('http_method,http_path', (
    ('GET', '/servers/'),
    ('POST', '/servers/'),
    ('GET', '/servers/1'),
    ('GET', '/servers/1'),
    ('DELETE', '/servers/1'),
    ('POST', '/servers/1/request'),
))
def test_general_access(http_method, http_path, flask_app_client):
    response = flask_app_client.open(method=http_method, path=http_path)
    assert response.status_code == 200
