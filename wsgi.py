"""
The app runner to be used for deployment via servers like Gunicorn or Waitress.
"""
from app import create_app

APP = create_app("production")
