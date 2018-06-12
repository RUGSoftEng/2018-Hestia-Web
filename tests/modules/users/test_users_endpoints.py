"""
Test user endpoints.
"""
import pytest

def test_POST_users(flask_app_client):
    """ Test that it is possible to access all of the user endpoints """
    http_method = 'POST'
    http_path = '/users/1'
    response = flask_app_client.open(method=http_method, path=http_path)
    print(response.get_json())
    assert response.get_json() is not None

def test_DELETE_users(flask_app_client):
    """ Test that it is possible to access all of the user endpoints """
    http_method = 'DELETE'
    http_path = '/users/1'
    response = flask_app_client.open(method=http_method, path=http_path)
    print(response.get_json())
    assert response.get_json() is not None
