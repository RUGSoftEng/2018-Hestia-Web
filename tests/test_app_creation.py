"""
Test application creation.
"""

from app import (create_app)

def test_create_app_default():
    """ Test creating the app using the default configuration. """
    try:
        create_app()
    except SystemExit:
        pass

def test_create_app_production():
    """ Test creating the app using the production configuration. """
    try:
        create_app('production')
    except SystemExit:
        pass

def test_create_app_development():
    """ Test creating the app using the development configuration. """
    try:
        create_app('development')
    except SystemExit:
        pass

def test_create_app_testing():
    """ Test creating the app using the testing configuration. """
    try:
        create_app('testing')
    except SystemExit:
        pass
