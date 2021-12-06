import enum

from sqlalchemy import Column, Integer, String, ForeignKey, Enum
from sqlalchemy.orm import relationship

from sql.alchemy import Base


class NodeType(enum. Enum):
    question = "question"
    answer = "answer"


class Quest(Base):
    __tablename__ = "quests"

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)


class Network(Base):
    __tablename__ = "networks"

    # Foreign
    fk_quest_id = ForeignKey(Quest.id)

    # Columns
    id = Column(Integer, primary_key=True)
    quest_id = Column(Integer, fk_quest_id)
    name = Column(String, nullable=False)

    # Relations
    quest = relationship(Quest, backref="networks")


class Node(Base):
    __tablename__ = "nodes"

    # Foreign
    fk_network_id = ForeignKey(Network.id)

    # Columns
    id = Column(Integer, primary_key=True)
    network_id = Column(Integer, fk_network_id)
    text = Column(String)
    type = Column(Enum(NodeType))

    # Relations
    network = relationship(Network, backref="nodes")


class Connection(Base):
    __tablename__ = "connections"

    # Foreign
    fk_node_in_id = ForeignKey(Node.id)
    fk_node_out_id = ForeignKey(Node.id)

    # Columns
    node_in_id = Column(Integer, fk_node_in_id, primary_key=True)
    node_out_id = Column(Integer, fk_node_out_id, primary_key=True)

    # Relations
    node_in = relationship(Node, foreign_keys=[fk_node_in_id], backref="connection_out")
    node_out = relationship(Node, foreign_keys=[fk_node_out_id], backref="connection_in")


if __name__ == "__main__":
    from sql.alchemy import engine
    from sqlalchemy_utils import database_exists, create_database

    if not database_exists(engine.url):
        create_database(engine.url)

    Base.metadata.create_all(engine)
