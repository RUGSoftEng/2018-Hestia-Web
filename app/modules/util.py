"""
Defines util functions to be accessed by modules.
"""
import base64
import uuid
import requests
from flask import (jsonify)

def url_safe_uuid():
    """
    Returns a url safe uuid.
    """
    return str(base64.urlsafe_b64encode(uuid.uuid4().bytes)).replace("=", "").replace("\'", "")[1:]

TIMEOUT = 1.0

def route_request(method, query, payload):
    """
    Defines the route function to send commands to a controller
    """
    method = method.upper()
    print("Sending request to server:", method, ", ", query, ", ", payload)
    if method == "GET":
        result = requests.get(query, verify=False, timeout=TIMEOUT).json()
    elif method == "POST":
        result = requests.post(query, verify=False,
                               json=payload, timeout=TIMEOUT).json()
    elif method == "PUT":
        result = requests.put(query, verify=False,
                              json=payload, timeout=TIMEOUT).json()
    elif method == "DELETE":
        result = requests.delete(query, verify=False, timeout=TIMEOUT)
    else:
        result = "Invalid REST method."
    return jsonify(result)
