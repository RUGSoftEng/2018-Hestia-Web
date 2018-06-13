"""
Test server endpoints general access.
"""
import pytest

@pytest.mark.parametrize('http_method,http_path', (
    ('GET', '/servers/'),
    ('POST', '/servers/'),
    ('GET', '/servers/1'),
    ('PUT', '/servers/1'),
    ('DELETE', '/servers/1'),
    ('POST', '/servers/1/ping'),
    ('POST', '/servers/1/batch_request'),
))
def test_no_access_for_unauthorized_users(http_method, http_path, flask_app_client):
    """
    Test that it is not possible to access any of the server endpoints
    if you are unauthorized.
    """
    response = flask_app_client.open(method=http_method, path=http_path)
    assert response.status_code == 401
