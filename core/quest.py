from pref import Preferences

from sql.models import Quest as QuestDB

from core.node import Node
from core.connection import Connection
from core.question import Question
from core.answer import Answer

import logging

logging.basicConfig(level=Preferences.logging_level_core)
logger = logging.getLogger(f"{Preferences.app_name} Quest")


class Quest(QuestDB):
    def get_owner(self):
        return self.owner

    def get_nodes(self):
        return self.nodes

    def get_connections(self):
        nodes = self.get_nodes()
        connections = [node.connections_out for node in nodes]
        return connections

    def create_node(self, node_cls, text: str):
        """Create node builder"""
        node = node_cls.create(quest_id=self.id, type=node_cls.node_type, text=text)
        return node

    def create_question(self, text: str):
        """Add question shortcut"""
        return self.create_node(Question, text)

    def create_answer(self, text: str):
        """Add answer shortcut"""
        return self.create_node(Answer, text)

    def connect_nodes(self, node_from: Node, node_to: Node):
        """Connect nodes"""
        if node_from.quest_id != node_to.quest_id:
            raise ValueError(f"Nodes {node_from} and {node_to} is not from same network")
        if node_from.quest_id != self.id:
            raise ValueError(f"Node {node_from} is not from this network")
        if node_to.quest_id != self.id:
            raise ValueError(f"Node {node_to} is not from this network")

        connection = Connection.create(node_in_id=node_from.id, node_out_id=node_to.id)
        return connection

    def get_starts(self):
        nodes = self.get_nodes()
        starts = list(filter(lambda node: not node.connections_in, nodes))
        return starts

    def get_ends(self):
        nodes = self.get_nodes()
        ends = list(filter(lambda node: not node.connections_out, nodes))
        return ends

    def show_debug_tree(self):
        starts = self.get_starts()

        for start_node in starts:
            logger.debug(self.get_tree_from(start_node))

    def get_tree_from(self, node: Node, depth: int = 0):
        text = ""
        if not node.connections_in:
            text = "(START) "

        text += f"«{node.text}»"
        node_out_connections = node.connections_out
        if node_out_connections:
            text += "-> "

        # Print linked blocks
        blocks = list()
        for connection in node_out_connections:
            next_node = connection.node_out
            blocks.append(f"«{next_node.text}»")

        text += "|".join(blocks)

        depth += 1

        for connection in node_out_connections:
            next_node = connection.node_out
            if next_node.connections_out:
                depth_text = depth * '\t'
                text += f"\n{depth_text}"
                text += self.get_tree_from(next_node, depth=depth)

        return text
