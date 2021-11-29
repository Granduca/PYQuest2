from pref import Preferences

import logging


logging.basicConfig(level=Preferences.logging_level_core)
logger = logging.getLogger(f"{Preferences.app_name} Network")


class Connection:
    def __init__(self):
        self.inputNode = None
        self.outputNode = None

    def set_connection(self, a, b):
        if not a:
            raise Exception('Input node is not specified.')
        if not b:
            raise Exception('Output node is not specified.')
        self.inputNode = a
        self.outputNode = b


class Network:
    def __init__(self):
        self._connections = []

    def add_connection(self, connection: Connection):
        if connection not in self._connections:
            self._connections.append(connection)
            connection.inputNode.add_connection(connection)
            connection.outputNode.add_connection(connection)
            connection.inputNode.set_depth()
            connection.outputNode.set_depth()
        else:
            logger.warning('This connection already exists')

    def remove_connection(self, connection: Connection):
        if connection in self._connections:
            self._connections.remove(connection)
            connection.inputNode.remove_connection(connection)
            connection.outputNode.remove_connection(connection)
            del connection
        else:
            logger.warning('This connection was not found')

    def get_network(self):
        return self._connections

    def print_network(self):
        for connection in self._connections:
            print(f'{connection.inputNode.text} - {connection.outputNode.text}')
