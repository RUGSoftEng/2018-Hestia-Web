"""
Declares the entity mapping between the database and python.
"""
import os

from datetime import (
    datetime
)

from sqlalchemy import (
    create_engine,
    Column,
    DateTime,
)

from sqlalchemy.ext.declarative import (
    declarative_base
)

from sqlalchemy.orm import (
    sessionmaker
)

DB_BASE_URL = 'localhost:5432'
DB_NAME = 'HestiaDB'
DB_USER = 'postgres'
DB_PASSWORD = 'hestia'
DB_URL = os.environ.get("DATABASE_URL",
                        (f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_BASE_URL}/{DB_NAME}'))

ENGINE = create_engine(DB_URL)

SESSION = sessionmaker(bind=ENGINE)

BASE = declarative_base()


class Entity:
    """
    A entity that is stored in a database.
    """
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

    def __init__(self):
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
