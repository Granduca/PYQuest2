import enum

from sqlalchemy import Column, Integer, String, ForeignKey, Enum
from sqlalchemy.orm import relationship

from sql.alchemy import Base


class NodeType(enum. Enum):
    question = "вопрос"
    answer = "ответ"

    def __str__(self):
        return self.value


class Quest(Base):
    __tablename__ = "quests"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)

    def __repr__(self):
        return f"<Quest({self.id}) «{self.title}»>"


class Network(Base):
    __tablename__ = "networks"

    # Foreign
    fk_quest_id = ForeignKey(Quest.id)

    # Columns
    id = Column(Integer, primary_key=True, autoincrement=True)
    quest_id = Column(Integer, fk_quest_id)
    name = Column(String, nullable=False)

    # Relations
    quest = relationship(Quest, foreign_keys=[quest_id], backref="networks")

    def __repr__(self):
        return f"<Network({self.id}) «{self.name}»>"


class Node(Base):
    __tablename__ = "nodes"

    # Foreign
    fk_network_id = ForeignKey(Network.id)

    # Columns
    id = Column(Integer, primary_key=True, autoincrement=True)
    network_id = Column(Integer, fk_network_id, nullable=False)
    text = Column(String)
    type = Column(Enum(NodeType))
    front_id = Column(Integer)

    # Relations
    network = relationship(Network, foreign_keys=[network_id], backref="nodes")

    def __repr__(self):
        return f"<Node({self.id}) {self.type} «{self.text}»>"


class NodeCoordinates(Base):
    __tablename__ = "nodes_coordinates"

    # Foreign
    fk_node_id = ForeignKey(Node.id)

    # Columns
    id = Column(Integer, fk_node_id, primary_key=True)
    x = Column(Integer, nullable=False)
    y = Column(Integer, nullable=False)

    # Relations
    node = relationship(Node, foreign_keys=[id], backref="coordinates")

    def __repr__(self):
        return f"<Coordinates({self.id}): {self.x}, {self.y}>"


class Connection(Base):
    __tablename__ = "connections"

    # Foreign
    fk_node_in_id = ForeignKey(Node.id)
    fk_node_out_id = ForeignKey(Node.id)

    # Columns
    node_in_id = Column(Integer, fk_node_in_id, primary_key=True)
    node_out_id = Column(Integer, fk_node_out_id, primary_key=True)

    # Relations
    node_in = relationship(Node, foreign_keys=[node_in_id], backref="connection_out")
    node_out = relationship(Node, foreign_keys=[node_out_id], backref="connection_in")

    def __repr__(self):
        return f"<Connection: {self.node_in} -> {self.node_out}>"


if __name__ == "__main__":
    """ Test database creation """
    from sql.alchemy import engine
    from sqlalchemy_utils import database_exists, create_database

    if not database_exists(engine.url):
        create_database(engine.url)

    Base.metadata.create_all(engine)

    from sql.alchemy import Session
    with Session.begin() as session:
        quest = Quest(title="Первый квест")
        session.add(quest)

        network = Network(name="New", quest=quest)
        session.add(network)
        node = Node(network=network)
        session.add(node)
        session.flush()
        print(quest)
        print(network)
        print(node)
        assert quest.id == 1, "Quest id is not 1"
        assert network.id == 1, "Network id is not 1"
        assert node.id == 1, "Node id is not 1"
        session.rollback()
