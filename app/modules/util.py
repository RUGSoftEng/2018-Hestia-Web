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

    # Fixes JS returning 0.0 and 1.0 as 0 and 1 respectively.
    if payload and "state" in payload and type(payload["state"]) == int:
        payload["state"] = float(payload["state"])

    print("Sending request to server:", method, ", ", query, ", ", payload)

    if method == "GET":
        result = requests.get(query, verify=False, timeout=TIMEOUT).json()
        print(result)
    elif method == "POST":
        result = requests.post(query, verify=False,
                               json=payload, timeout=TIMEOUT).json()
    elif method == "PUT":
        result = requests.put(query, verify=False,
                              json=payload, timeout=TIMEOUT).json()
    elif method == "DELETE":
        result = requests.delete(query, verify=False, timeout=TIMEOUT).text
    else:
        result = "Invalid REST method."

    return jsonify(result)

def ping(query):
    """
    Ping a URL and return the time.
    """
    return {
            "value" : requests.options(query, verify=False, timeout=TIMEOUT).elapsed.microseconds/1000.0,
            "unit" : "ms",
    }
