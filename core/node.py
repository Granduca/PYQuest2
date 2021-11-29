from . import Connection
from pref import Preferences

import logging


logging.basicConfig(level=Preferences.logging_level_core)
logger = logging.getLogger(f"{Preferences.app_name} Node")


class Node:
    def __init__(self):
        self.is_start = False
        self.is_end = False
        self._network = None
        self._text = ''
        self._depth = 0
        self._connections = []

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

    def get_connection(self):
        return self._connections

    def add_connection(self, connection):
        if connection not in self._connections:
            self._connections.append(connection)

    def _set_connection(self, a, b):
        if self._network:
            c = Connection()
            c.set_connection(a, b)
            self._network.add_connection(c)
        else:
            raise Exception('First, you must specify the network for this node!')

    def remove_connection(self, connection):
        if connection in self._connections:
            self._connections.remove(connection)

    def get_depth(self):
        return self._depth

    def set_depth(self):
        if not self._network:
            self._depth = 0
            self.is_start = True
        else:
            depth_map = []
            for connection in self._connections:
                if connection.outputNode == self:
                    depth_map.append(connection.inputNode.get_depth())
            if depth_map:
                depth_map.sort(reverse=True)
                self._depth = depth_map[0] + 1
                self.is_start = False
            else:
                self._depth = 0
                self.is_start = True

    def get_child(self):
        child = []

        if self._network:
            if self._connections:
                for connection in self._connections:
                    if connection.inputNode == self:
                        child.append(connection.outputNode)
        else:
            raise Exception('First, you must specify the network for this node!')

        return child

    def set_child(self, child):
        self._set_connection(self, child)

    def get_parent(self):
        parent = []

        if self._network:
            if self._connections:
                for connection in self._connections:
                    if connection.outputNode == self:
                        parent.append(connection.inputNode)
        else:
            raise Exception('First, you must specify the network for this node!')

        return parent

    def set_parent(self, parent):
        self._set_connection(parent, self)

    def disconnect(self):
        if self._network:
            if self._connections:
                for connection in self._connections:
                    if connection.inputNode == self:
                        self._network.remove_connection(connection)
                    if connection.outputNode == self:
                        self._network.remove_connection(connection)
            self._network = None

    def get_tree(self, **kwargs):
        divider = '.\t'
        end = ''
        start = ''

        if 'divider' in kwargs:
            divider = kwargs['divider']

        if self.is_start:
            start = '(START) '
        if self.is_end:
            end = ' (END)'
        logger.info(f"TREE:{divider*self.get_depth()}{start}{self.text}{end}")

        if self.get_child():
            for child in self.get_child():
                child.get_tree(divider=divider)


class GroupNode(Node):
    def __init__(self):
        super().__init__()

    def disconnect(self):
        if self._network:
            if self._connections:
                for connection in self._connections:
                    if connection.outputNode == self:
                        self._network.remove_connection(connection)
                    if connection.inputNode == self:
                        for c in connection.outputNode.get_connection():
                            if c.inputNode == connection.outputNode:
                                self._network.remove_connection(c)
            self._network = None

