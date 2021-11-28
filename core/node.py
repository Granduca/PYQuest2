from . import Connection
from pref import Preferences

import logging


logging.basicConfig(level=Preferences.logging_level_core)
logger = logging.getLogger(f"{Preferences.app_name} Node")


class GroupNode:
    def __init__(self):
        self._network = None
        self.is_start = False
        self.is_end = False
        self._text = ''

    def disconnect(self):
        if self._network:
            if self._network.get_network():
                for connection in self._network.get_network():
                    if connection.outputNode == self:
                        self._network.remove_connection(connection)
                    if connection.inputNode == self:
                        for c in self._network.get_network():
                            if c.inputNode == connection.outputNode:
                                self._network.remove_connection(c)
            self._network = None


class Node:
    def __init__(self):
        self._network = None
        self.is_start = False
        self.is_end = False
        self._text = ''

    def set_child(self, child):
        if self._network:
            c = Connection()
            c.set_connection(self, child)
            self._network.add_connection(c)
        else:
            raise Exception('First, you must specify the network for this node!')

    def set_parent(self, parent):
        if self._network:
            c = Connection()
            c.set_connection(parent, self)
            self._network.add_connection(c)
        else:
            raise Exception('First, you must specify the network for this node!')

    def get_childs(self):

        childs = []

        if self._network:
            if self._network.get_network():
                for connection in self._network.get_network():
                    if connection.inputNode == self:
                        childs.append(connection.outputNode)
        else:
            raise Exception('First, you must specify the network for this node!')

        return childs

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, text: str):
        self._text = text

    @property
    def network(self):
        return self._network

    @network.setter
    def network(self, network):
        if self._network:
            self.disconnect()
        self._network = network

    def disconnect(self):
        if self._network:
            if self._network.get_network():
                for connection in self._network.get_network():
                    if connection.inputNode == self:
                        self._network.remove_connection(connection)
                    if connection.outputNode == self:
                        self._network.remove_connection(connection)
            self._network = None

    def get_tree(self, **kwargs):
        node_from = self
        depth = 1
        divider = '.\t'

        if 'node_from' in kwargs:
            node_from = kwargs['node_from']
        if 'depth' in kwargs:
            depth = kwargs['depth']
        if 'divider' in kwargs:
            divider = kwargs['divider']

        logger.info(f"TREE:{divider*depth}{self.text}")

        if self.get_childs():
            for child in self.get_childs():
                if not self.is_end:
                    if child != node_from:
                        child.get_tree(node_from=node_from, depth=depth+1, divider=divider)
                    else:
                        logger.info(f"TREE:{divider*(depth+1)}<--")
                else:
                    logger.info(f"TREE:{divider * (depth+1)}END")
