from pref import Preferences

from .base import DatabaseObject

from sql.models import Network as NetworkDB
from sql.models import Connection as ConnectionDB

from sql.database import Session

import logging


logging.basicConfig(level=Preferences.logging_level_core)
logger = logging.getLogger(f"{Preferences.app_name} Network")


class Connection(DatabaseObject):
    db_object = ConnectionDB
    session = Session

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


class Network(DatabaseObject):
    db_object = NetworkDB
    session = Session

    def __init__(self, quest_id: int, name: str = "Default", network_id: int = None):
        self.id = network_id
        self.quest_id = quest_id
        self.name = name
        self._connections = list()

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

    def save(self):
        save_object = self.db_object(name=self.name, quest_id=self.quest_id)
        with self.session() as session:
            session.add(save_object)
            session.commit()

        self.id = save_object.id

    def update(self):
        pass

    @classmethod
    def load(cls, network_id: int):
        with cls.session as session:
            network_db = session.query(cls.db_object).filter_by(id=network_id).one()

        return cls(network_db.id)
