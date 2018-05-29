"""
Test user endpoints.
"""
import pytest


@pytest.mark.parametrize('http_method,http_path', (
    ('POST', '/users/'),
    ('DELETE', '/users/1'),
))
def test_POST_users(http_method, http_path, flask_app_client):
    """ Test that it is possible to access all of the user endpoints """
    response = flask_app_client.open(method=http_method, path=http_path)
    print(response.get_json())
    assert response.get_json() is not None

def test_DELETE_users(http_method, http_path, flask_app_client):
    """ Test that it is possible to access all of the user endpoints """
    response = flask_app_client.open(method=http_method, path=http_path)
    print(response.get_json())
    assert response.get_json() is not None
