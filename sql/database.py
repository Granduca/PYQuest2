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
    metadata.create_all(bind=engine)
