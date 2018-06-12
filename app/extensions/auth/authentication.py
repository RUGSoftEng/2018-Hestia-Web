"""
Provides an authentication layer using JWT via Auth0.
"""
from functools import (wraps)
from os import (environ as env)
from six.moves.urllib.request import (urlopen)
from dotenv import (
    load_dotenv,
    find_dotenv,
)
from flask import (
    request,
    jsonify,
    _request_ctx_stack,
    json,
)
from jose import (jwt)

from ..api import (API)

ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)
AUTH0_DOMAIN = env.get("AUTH0_DOMAIN")
API_IDENTIFIER = env.get("API_IDENTIFIER")
ALGORITHMS = ["RS256"]

def auth_class_factory(BaseClass):
    class AuthClass(BaseClass):
        def __init__(self, *args, **kwargs):
            super(AuthClass, self).__init__(*args, **kwargs)
    return AuthClass

class AuthError(Exception):
    """
    An error to be thrown when unauthenticated access to protected resource is requested.
    """
    def __init__(self, error, status_code):
        Exception.__init__(self)
        self.error = error
        self.status_code = status_code

@API.errorhandler(AuthError)
def handle_auth_error(ex):
    """
    Produce the authentication error as a JSON HTTP response.
    """
    response = jsonify(ex.error)
    response.status_code = ex.status_code
    return restplus_error_wrapper(response)

def restplus_error_wrapper(error_response):
    """
    Wrapper for returning auth error to compatible with restplus exceptions
    """
    return json.loads(error_response.get_data()), error_response.status_code

def get_token_auth_header():
    """Obtains the access token from the Authorization Header
    """
    auth = request.headers.get("Authorization", None)
    if not auth:
        raise AuthError({"code": "authorization_header_missing",
                         "description":
                         "Authorization header is expected"}, 401)

    parts = auth.split()

    if parts[0].lower() != "bearer":
        raise AuthError({"code": "invalid_header",
                         "description":
                         "Authorization header must start with"
                         " Bearer"}, 401)
    elif len(parts) == 1:
        raise AuthError({"code": "invalid_header",
                         "description": "Token not found"}, 401)
    elif len(parts) > 2:
        raise AuthError({"code": "invalid_header",
                         "description":
                         "Authorization header must be"
                         " Bearer token"}, 401)

    token = parts[1]
    return token

class Authenticator():
    """
    TODO: change this comment
    A class for authentication functions
    """
   
    def get_user_id(self):
        """
        Get the user id from the access token in the Authorization header.
        """
        token = get_token_auth_header()
    
        jsonurl = urlopen("https://"+AUTH0_DOMAIN+"/.well-known/jwks.json")
    
        jwks = json.loads(jsonurl.read())
    
        rsa_key = {}
        for key in jwks["keys"]:
            rsa_key = {
                "kty": key["kty"],
                "kid": key["kid"],
                "use": key["use"],
                "n": key["n"],
                "e": key["e"]
            }
    
        payload = jwt.decode(
            token,
            rsa_key,
            algorithms=ALGORITHMS,
            audience=API_IDENTIFIER,
            issuer="https://"+AUTH0_DOMAIN+"/"
        )
    
        return payload['sub']
    
    def requires_auth(self, func):
        """Determines if the access token is valid
        """
        @wraps(func)
        def decorated(*args, **kwargs):
            """
            The decorator requiring authentication before func may be called.
            """
            token = get_token_auth_header()
            jsonurl = urlopen("https://"+AUTH0_DOMAIN+"/.well-known/jwks.json")
            jwks = json.loads(jsonurl.read())
            try:
                unverified_header = jwt.get_unverified_header(token)
            except jwt.JWTError:
                raise AuthError({"code": "invalid_header",
                                 "description":
                                 "Invalid header. "
                                 "Use an RS256 signed JWT Access Token"}, 401)
            if unverified_header["alg"] == "HS256":
                raise AuthError({"code": "invalid_header",
                                 "description":
                                 "Invalid header. "
                                 "Use an RS256 signed JWT Access Token"}, 401)
            rsa_key = {}
            for key in jwks["keys"]:
                if key["kid"] == unverified_header["kid"]:
                    rsa_key = {
                        "kty": key["kty"],
                        "kid": key["kid"],
                        "use": key["use"],
                        "n": key["n"],
                        "e": key["e"]
                    }
            if rsa_key:
                try:
                    payload = jwt.decode(
                        token,
                        rsa_key,
                        algorithms=ALGORITHMS,
                        audience=API_IDENTIFIER,
                        issuer="https://"+AUTH0_DOMAIN+"/"
                    )
                except jwt.ExpiredSignatureError:
                    raise AuthError({"code": "token_expired",
                                     "description": "token is expired"}, 401)
                except jwt.JWTClaimsError:
                    raise AuthError({"code": "invalid_claims",
                                     "description":
                                     "incorrect claims,"
                                     " please check the audience and issuer"}, 401)
                except Exception:
                    raise AuthError({"code": "invalid_header",
                                     "description":
                                     "Unable to parse authentication"
                                     " token."}, 401)
    
                _request_ctx_stack.top.current_user = payload
                return func(*args, **kwargs)
            raise AuthError({"code": "invalid_header",
                             "description": "Unable to find appropriate key"}, 401)
        return decorated

class AuthenticatorTest():
    """
    A fake authentication class for testing authenticated requests.
    """

    def __init__(self, user_id):
        self.user_id = user_id

    def get_user_id(self):
        """
        Get a hardcoded user id for testing.
        """
        return self.user_id

    def requires_auth(self, func):
        """
        Override the default decorator to allow authenticated usage.
        """
        @wraps(func)
        def decorated(*args, **kwargs):
            """
            Override the default decorator to facilitate testing.
            """
            token = get_token_auth_header()
            return func(*args, **kwargs)
        return decorated



