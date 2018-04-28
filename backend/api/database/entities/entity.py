"""
Declares the entity mapping between the database and python.
"""
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, DateTime, event
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlite3 import dbapi2 as sqlite

DB_URL = 'localhost:5432'
DB_NAME = 'HestiaDB'
DB_USER = 'postgres'
DB_PASSWORD = 'hestia'
ENGINE = create_engine(
    f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_URL}/{DB_NAME}')

## Exploring using SQLite
# ENGINE = create_engine('sqlite+pysqlite:///hestia.db', module=sqlite)
# def _fk_pragma_on_connect(dbapi_con, con_record):
#     dbapi_con.execute('pragma foreign_keys=ON')

# event.listen(ENGINE, 'connect', _fk_pragma_on_connect)
## End SQLite exploration

SESSION = sessionmaker(bind=ENGINE)


BASE = declarative_base()


class Entity():  # pylint: disable=too-few-public-methods
    """
    A entity that is stored in a database.
    """
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

    def __init__(self):
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
