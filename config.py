"""
Declare application configuration.
"""
import os

DB_BASE_URL = 'localhost:5432'
DB_USER = 'postgres'
DB_PASSWORD = 'hestia'

class BaseConfig:
    """ Base configuration options for the application. """
    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(BaseConfig):
    """ Development configuration for the application. """
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///HestiaDB'
    PORT = 5000


class TestingConfig(BaseConfig):
    """ Test related configuration for the application. """
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///HestiaDB'
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    PORT = 5000


class ProductionConfig(BaseConfig):
    """ Production configuration for the application. """
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///HestiaDBA'
    PORT = int(os.environ.get("PORT", 5000))


CONFIG_MAPPER = dict(
    development=DevelopmentConfig,
    testing=TestingConfig,
    production=ProductionConfig,
)
