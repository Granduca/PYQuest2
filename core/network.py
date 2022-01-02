
from typing import Set, List

from pref import Preferences

from sql.database import Session
from sql.models import Network as NetworkDB
from sql.models import Network as NodeDB
from sql.models import Connection as ConnectionDB

from core.base import DatabaseObject
from core.node import Node
from core.question import Question
from core.answer import Answer

import logging


logging.basicConfig(level=Preferences.logging_level_core)
logger = logging.getLogger(f"{Preferences.app_name} Network")


class Connection(DatabaseObject):
    db_object = ConnectionDB
    session = Session

    def __init__(self, node_in: Node, node_out: Node):
        self.input_node = node_in
        self.output_node = node_out

    def save(self):
        save_object = self.db_object(node_in_id=self.input_node.id, node_out_id=self.output_node.id)
        with self.session() as session:
            session.add(save_object)
            session.commit()

    def update(self):
        pass

    @classmethod
    def load(cls, node_in: Node, node_out: Node):
        with cls.session() as session:
            session.query(cls.db_object).filter_by(node_in_id=node_in.id, node_out_id=node_out.id).one()
            connection = cls(node_in, node_out)

        return connection


class Network(DatabaseObject):
    db_object = NetworkDB
    session = Session

    def __init__(self, quest, name: str = "Default", network_id: int = None):
        self.id = network_id
        self.quest = quest
        self.name = name
        self.nodes: Set[Node] = set()
        self.connections: Set[Connection] = set()

    def add_node(self, node):
        self.nodes.add(node)

    def get_nodes(self):
        return self.nodes

    def extend_nodes(self, nodes_db: List[NodeDB]):
        for node_db in nodes_db:
            node = Node(self, text=node_db, node_id=node_db.id)
            self.nodes.add(node)
            # TODO Restore connections
            # TODO Create connections between nodes

    def create_node(self, node_cls, text: str):
        node = node_cls(self, text)
        node.save()
        # TODO if not connected = create connect
        return node

    def create_connection(self, node_in: Node, node_out: Node):
        connection = Connection(node_in, node_out)
        connection.save()
        self.connections.add(connection)

    def create_question(self, text: str):
        """Add question shortcut"""
        return self.create_node(Question, text)

    def create_answer(self, text: str):
        """Add answer shortcut"""
        return self.create_node(Answer, text)

    def save(self):
        save_object = self.db_object(name=self.name, quest_id=self.quest.id)
        with self.session() as session:
            session.add(save_object)
            session.commit()
            self.id = save_object.id

    def update(self):
        update_object = self.db_object(id=self.id, name=self.name, quest_id=self.quest.id)
        with self.session() as session:
            session.add(update_object)
            session.commit()

    @classmethod
    def load(cls, quest, network_id: int):
        with cls.session() as session:
            network_db = session.query(cls.db_object).filter_by(id=network_id).one()
            network = cls(quest)
            network.id = network_db.id
            network.name = network_db.name
            nodes_db = network_db.nodes
            network.extend_nodes(nodes_db)
        return network
