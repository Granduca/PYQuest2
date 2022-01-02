from pref import Preferences

from sql.models import Node as NodeDB
from sql.models import NodeType
from sql.database import Session

from core.base import DatabaseObject

import logging


logging.basicConfig(level=Preferences.logging_level_core)
logger = logging.getLogger(f"{Preferences.app_name} Node")


class Node(DatabaseObject):
    db_object = NodeDB
    session = Session
    type: NodeType

    def __init__(self, network, text: str, node_id: int = None):
        self.id = node_id
        self.text = text
        self.network = network
        self._attach_to_network()

    def _attach_to_network(self):
        self.network.add_node(self)

    def save(self):
        save_object = self.db_object(text=self.text, type=self.type, network_id=self.network.id)
        with self.session() as session:
            session.add(save_object)
            session.commit()
            self.id = save_object.id

    def update(self):
        save_object = self.db_object(id=self.id, text=self.text, type=self.type, network_id=self.network.id)
        with self.session() as session:
            session.add(save_object)
            session.commit()

    @classmethod
    def load(cls, network, node_id: int):
        """Load Quest object from database"""
        with cls.session() as session:
            node_db = session.query(cls.db_object).filter_by(id=node_id).one()
            node = cls(network, node_db.text)
            node.id = node_db.id
            node.type = node_db.type
        return node
