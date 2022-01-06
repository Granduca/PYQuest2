import enum

from sqlalchemy import Column, Integer, String, ForeignKey, Enum
from sqlalchemy.orm import relationship

from sql.database import Base, ActiveRecordMixin


class NodeType(enum. Enum):
    question = "вопрос"
    answer = "ответ"

    def __str__(self):
        return self.value


class User(Base, ActiveRecordMixin):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    role = Column(String, nullable=False)
    telegram_id = Column(Integer)
    google_id = Column(Integer)


class Quest(Base, ActiveRecordMixin):
    """
    Main quest object
    Keeps list of networks
    """
    __tablename__ = "quests"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)

    def __repr__(self):
        return f"<Quest({self.id}) «{self.title}»>"


class Node(Base, ActiveRecordMixin):
    """
    Node of quest
    Represents basic object of quest
    """
    __tablename__ = "nodes"

    # Foreign
    fk_quest_id = ForeignKey(Quest.id)

    # Columns
    id = Column(Integer, primary_key=True, autoincrement=True)
    quest_id = Column(Integer, fk_quest_id, nullable=False)
    text = Column(String)
    type = Column(Enum(NodeType))

    # Relations
    quest = relationship(Quest, foreign_keys=[quest_id], backref="nodes")

    __mapper_args__ = {'polymorphic_on': type}

    def __repr__(self):
        return f"<{self.__class__.__name__}({self.id}) {self.type} «{self.text}»>"


class NodeAttributes(Base, ActiveRecordMixin):
    """Coordinates of node"""
    __tablename__ = "nodes_coordinates"

    # Foreign
    fk_node_id = ForeignKey(Node.id)

    # Columns
    id = Column(Integer, fk_node_id, primary_key=True)
    x = Column(Integer, nullable=False)
    y = Column(Integer, nullable=False)
    height = Column(Integer)

    # Relations
    node = relationship(Node, foreign_keys=[id], backref="attributes")

    def __repr__(self):
        return f"<Attributes({self.id}): {self.x}, {self.y}>"


class Connection(Base, ActiveRecordMixin):
    """Connection between two nodes"""
    __tablename__ = "connections"

    # Foreign
    fk_node_in_id = ForeignKey(Node.id)
    fk_node_out_id = ForeignKey(Node.id)

    # Columns
    node_in_id = Column(Integer, fk_node_in_id, primary_key=True)
    node_out_id = Column(Integer, fk_node_out_id, primary_key=True)

    # Relations
    node_in = relationship(Node, foreign_keys=[node_in_id], backref="connections_out")
    node_out = relationship(Node, foreign_keys=[node_out_id], backref="connections_in")

    def __repr__(self):
        return f"<Connection {self.node_in} -> {self.node_out}>"
