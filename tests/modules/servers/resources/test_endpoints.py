"""
Test server endpoints
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

def test_general_return(http_method, http_path, flask_app_client):
    response = flask_app_client.open(method=http_method, path=http_path)
    print(response.get_json())
    assert response is not None

def test_GET_servers(flask_app_client):
    response = flask_app_client.open(method='GET', path='/servers/')
    print(response.get_json())
    assert response is not None

def test_POST_servers(flask_app_client):
    response = flask_app_client.open(method='POST', path='/servers/')
    print(response.get_json())
    assert response is not None

def test_GET_server(flask_app_client):
    server_id = "test_server"
    response = flask_app_client.open(method='GET', path=f'/servers/{server_id}')
    print(response.get_json())
    assert response is not None

def test_PUT_server(flask_app_client):
    server_id = "test_server"
    response = flask_app_client.open(method='PUT', path=f'/servers/{server_id}')
    print(response.get_json())
    assert response is not None

def test_DELETE_server(flask_app_client):
    server_id = "test_server"
    response = flask_app_client.open(method='DELETE', path=f'/servers/{server_id}')
    print(response.get_json())
    assert response is not None

def test_POST_server_ping(flask_app_client):
    server_id = "test_server"
    response = flask_app_client.open(method='POST', path=f'/servers/{server_id}/ping')
    print(response.get_json())
    assert response is not None

def test_POST_server_batch_request(flask_app_client):
    server_id = "test_server"
    response = flask_app_client.open(method='POST', path=f'/servers/{server_id}/batch_request')
    print(response.get_json())
    assert response is not None
