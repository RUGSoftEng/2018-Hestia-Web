"""
Test user endpoints.
"""
import pytest


@pytest.mark.parametrize('http_method,http_path', (
    ('POST', '/users/'),

))
def test_general_access(http_method, http_path, flask_app_client):
    response = flask_app_client.open(method=http_method, path=http_path)
    assert response.status_code == 200
