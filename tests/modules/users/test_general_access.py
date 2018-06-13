"""
Test user access
"""
import pytest

@pytest.mark.parametrize('http_method, http_path', (
    ('POST', '/users/'),
    ('DELETE', '/users/'),
))
def test_no_access_for_unauthorized_users(http_method, http_path, flask_app_client):
    """ Test that unauthorized users may not access these endpoints. """
    response = flask_app_client.open(method=http_method, path=http_path)
    assert response.status_code == 401
