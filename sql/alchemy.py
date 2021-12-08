from sqlalchemy import MetaData
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


def configure_metadata():
    naming_convention = {
        "ix": 'ix_%(column_0_label)s',
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s"
    }

    metadata_obj = MetaData(naming_convention=naming_convention)
    return metadata_obj


db_path = "../data/quest.sqlite"
engine = create_engine(f'sqlite:///{db_path}')
Base = declarative_base(metadata=configure_metadata())
Session = sessionmaker(bind=engine)
