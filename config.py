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
    SQLALCHEMY_DATABASE_URI = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_BASE_URL}/HestiaDB'
    PORT = 5000


class TestingConfig(BaseConfig):
    """ Test related configuration for the application. """
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_BASE_URL}/HestiaTestDB'
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    PORT = 5000


class ProductionConfig(BaseConfig):
    """ Production configuration for the application. """
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
        f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_BASE_URL}/HestiaDB'
    )
    PORT = int(os.environ.get("PORT", 5000))


CONFIG_MAPPER = dict(
    development=DevelopmentConfig,
    testing=TestingConfig,
    production=ProductionConfig,
)
