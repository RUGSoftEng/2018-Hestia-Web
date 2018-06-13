"""
Test application creation.
"""

from app import (create_app)

def test_create_app_default():
    """ Test creating the app using the default configuration. """
    try:
        app = create_app()
    except SystemExit:
        pass
    assert(app.config['ENV'] == "development")
    assert(app.config['DEBUG'] is True)
    assert(app.config['TESTING'] is False)

def test_create_app_development():
    """ Test creating the app using the development configuration. """
    try:
        app = create_app('development')
    except SystemExit:
        pass
    assert(app.config['ENV'] == "development")
    assert(app.config['DEBUG'] is True)
    assert(app.config['TESTING'] is False)

def test_create_app_testing():
    """ Test creating the app using the testing configuration. """
    try:
        app = create_app('testing')
    except SystemExit:
        pass
    assert(app.config['ENV'] == "testing")
    assert(app.config['DEBUG'] is True)
    assert(app.config['TESTING'] is True)
