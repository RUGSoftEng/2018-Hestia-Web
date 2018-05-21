"""
Test user endpoints.
"""
import pytest


@pytest.mark.parametrize('http_method,http_path', (
    ('POST', '/users/'),
))
def test_general_access(http_method, http_path, flask_app_client):
    """ Test that it is possible to access all of the user endpoints """
    response = flask_app_client.open(method=http_method, path=http_path)
    print(response.get_json())
    assert response.get_json() == "Posting user"
