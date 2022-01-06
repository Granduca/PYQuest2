from pref import Preferences

from sql.models import Node as NodeDB
from core.connection import Connection

import logging


logging.basicConfig(level=Preferences.logging_level_core)
logger = logging.getLogger(f"{Preferences.app_name} Node")


class Node(NodeDB):
    def set_child(self, node):
        return Connection.create(node_in_id=self.id, node_out_id=node.id)
