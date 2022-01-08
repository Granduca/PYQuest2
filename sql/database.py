import os

from sqlalchemy import MetaData
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.engine import Engine
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy_mixins.activerecord import ActiveRecordMixin

naming_convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

database_url = os.environ.get('DATABASE_URL', "sqlite:///")
engine = create_engine(database_url)
metadata = MetaData(naming_convention=naming_convention)
Base = declarative_base(metadata=metadata)
session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)

# Конфигурируем сессию для Session Mixin
ActiveRecordMixin.set_session(Session())


def create_db(_engine: Engine = None):
    """Create database"""
    import os.path
    from sqlalchemy_utils import database_exists, create_database

    _engine = _engine or engine
    engine_url = _engine.url
    engine_path = engine_url.database
    if engine_path and engine_path != ":memory:":
        dir_name = os.path.dirname(engine_path)
        if dir_name and not os.path.exists(dir_name):
            os.mkdir(dir_name)

    if not database_exists(engine_url):
        create_database(engine_url)


def init_db(bind: Engine):
    """Initialize database"""
    # Importing models
    # noinspection PyUnresolvedReferences
    import sql.models

    metadata.create_all(bind=bind)
