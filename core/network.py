from pref import Preferences

from sql.models import Network as NetworkDB

from core.node import Node
from core.connection import Connection
from core.question import Question
from core.answer import Answer

import logging


logging.basicConfig(level=Preferences.logging_level_core)
logger = logging.getLogger(f"{Preferences.app_name} Network")


class Network(NetworkDB):
    def get_nodes(self):
        return self.nodes

    def create_node(self, node_cls, text: str):
        node = node_cls.create(network_id=self.id, type=node_cls._type, text=text)
        node.save()
        return node

    def create_question(self, text: str):
        """Add question shortcut"""
        return self.create_node(Question, text)

    def create_answer(self, text: str):
        """Add answer shortcut"""
        return self.create_node(Answer, text)

    def connect_nodes(self, node_from: Node, node_to: Node):
        if node_from.network_id != node_to.network_id:
            raise ValueError(f"Nodes {node_from} and {node_to} is not from same network")
        if node_from.network_id != self.id:
            raise ValueError(f"Node {node_from} is not from this network")
        if node_to.network_id != self.id:
            raise ValueError(f"Node {node_to} is not from this network")

        return Connection.create(node_in_id=node_from.id, node_out_id=node_to.id)
