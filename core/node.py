from pref import Preferences

import logging


logging.basicConfig(level=Preferences.logging_level_core)
logger = logging.getLogger(f"{Preferences.app_name} Node")


class Network:
    def __init__(self):
        self._connections = []

    def add_connection(self, connection):
        self._connections.append(connection)

    def remove_connection(self, connection):
        self._connections.remove(connection)
        del connection

    def get_network(self):
        return self._connections

    def print_network(self):
        for connection in self._connections:
            print(f'{connection.inputNode.text} - {connection.outputNode.text}')


class Connection:
    def __init__(self):
        self.inputNode = None
        self.outputNode = None

    def set_connection(self, a, b):
        if not a:
            logger.error('Input node is not specified.')
            return
        if not b:
            logger.error('Output node is not specified.')
            return
        self.inputNode = a
        self.outputNode = b


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
    def text(self, text):
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
