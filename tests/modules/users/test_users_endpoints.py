"""
Test user endpoints.
"""

def test_post_users(flask_app_authenticated_client):
    """ Testing that posting a user functions. """
    http_method = 'post'
    http_path = '/users/'

    response = flask_app_authenticated_client.open(method=http_method, path=http_path, headers={'authorization':'bearer 1'})
    assert(response.get_json() == {'user_id' : '1'})
    assert response.status_code == 200

def test_delete_users(flask_app_authenticated_client_in_DB):
    """ Test that deleting a user functions. """
    http_method = 'delete'
    http_path = '/users/'

    response = flask_app_authenticated_client_in_DB.open(method=http_method, path=http_path, headers={'authorization':'bearer 1'})
    assert response.status_code == 204

def test_delete_non_existant_user(flask_app_authenticated_client):
    """ Test that deleting a non existant user results in a 404 """
    http_method = 'delete'
    http_path = '/users/'

    response = flask_app_authenticated_client.open(method=http_method, path=http_path, headers={'authorization':'bearer 1'})
    assert response.status_code == 404
