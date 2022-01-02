from pref import Preferences

from sql.models import Network as NetworkDB
from sql.models import Connection as ConnectionDB

from core.question import Question
from core.answer import Answer

import logging


logging.basicConfig(level=Preferences.logging_level_core)
logger = logging.getLogger(f"{Preferences.app_name} Network")


class Connection(ConnectionDB):
    pass


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
