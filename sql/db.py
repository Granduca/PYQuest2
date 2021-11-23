from sql.user import User
from sql.schema.schema import TNode

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base


class DB:
    def __init__(self, user: User):
        self._user = user
        self._db_path = 'data/pyquest2'
        self._engine = create_engine(f'sqlite:///{self._db_path}.db')
        self._base = declarative_base()
        # self._session = self._create_session()

    # def _db_session(func):
    #     @wraps(func)
    #     def wrapper(self):
    #         with self._session.begin() as session:
    #             func(self)
    #         session.commit()
    #     return wrapper

    # def _create_session(self):
    #     Session = sessionmaker()
    #     Session.configure(bind=self._engine)
    #     session = Session()
    #     return session

    def create_base_tables(self):
        self._base.metadata.create_all(self._engine, TNode.metadata.tables.values())
