"""
Declares the entity mapping between the database and python.
"""

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

DB_URL = 'localhost:5432'
DB_NAME = 'HestiaDB'
DB_USER = 'postgres'
DB_PASSWORD = 'hestia'
ENGINE = create_engine(
    f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_URL}/{DB_NAME}')

SESSION = sessionmaker(bind=ENGINE)


BASE = declarative_base()


class Entity():
    """
    A entity that is stored in a database.
    """
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

    def __init__(self):
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
