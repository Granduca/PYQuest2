from sqlalchemy import MetaData
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from pref.prefs import Preferences


naming_convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}


engine = create_engine(Preferences.SQLALCHEMY_DATABASE_URI)
metadata = MetaData(naming_convention=naming_convention)
Base = declarative_base(metadata=metadata)
Session = sessionmaker(bind=engine)


def init_db():
    """Initialize database"""
    import os.path
    from sqlalchemy_utils import database_exists, create_database

    engine_url = engine.url
    engine_path = engine_url.database
    if not os.path.exists(os.path.dirname(engine_path)):
        os.mkdir(os.path.dirname(engine_path))
    if not database_exists(engine_url):
        create_database(engine_url)

    # Importing models
    # noinspection PyUnresolvedReferences
    import sql.models

    metadata.create_all(bind=engine)
