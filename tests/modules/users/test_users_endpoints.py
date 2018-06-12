"""
Test user endpoints.
"""
import pytest

def test_post_users(flask_app_authenticated_client):
    """ test that it is possible to access all of the user endpoints """
    http_method = 'post'
    http_path = '/users/'
    response = flask_app_authenticated_client.open(method=http_method, path=http_path, headers={'authorization':'bearer 1'})
    assert(response.get_json() == {'user_id' : '1'})
    assert response.status_code == 200

def test_delete_users(flask_app_authenticated_client_in_DB):
    """ test that it is possible to access all of the user endpoints """
    http_method = 'delete'
    http_path = '/users/1'

    response = flask_app_authenticated_client.open(method=http_method, path=http_path, headers={'authorization':'bearer 1'})
    assert response.status_code == 204
