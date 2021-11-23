from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Table, Column, Integer, String


Base = declarative_base()


class TUser(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    password = Column(String)


class TNode(Base):
    __tablename__ = "node"
    id = Column(Integer, primary_key=True)
    type = Column(String)
    in_ports = Column(String)
    out_ports = Column(String)
