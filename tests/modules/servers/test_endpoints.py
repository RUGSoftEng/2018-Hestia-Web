"""
Test server endpoints
"""
import pytest

def test_GET_servers(flask_app_authenticated_client_in_DB_with_server):
    """ Test that getting your servers functions. """
    response = flask_app_authenticated_client_in_DB_with_server.open(method='GET', path='/servers/',  headers={'authorization':'bearer 1'})
    result = response.get_json()[0]
    assert(result["server_id"] is not None)
    assert(result["server_port"] == "string")
    assert(result["server_address"] == "string")
    assert(result["server_name"] == "string")
    assert(result["user_id"] == "1")
    assert(response.status_code == 200)
