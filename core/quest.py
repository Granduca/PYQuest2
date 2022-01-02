from typing import List

from pref import Preferences

from core.base import DatabaseObject
from core.network import Network

from sql.models import Quest as QuestDB
from sql.models import Network as NetworkDB
from sql.database import Session


import logging

logging.basicConfig(level=Preferences.logging_level_core)
logger = logging.getLogger(f"{Preferences.app_name} Quest")


class Quest(DatabaseObject):
    db_object = QuestDB
    session = Session

    def __init__(self, title: str):
        self.id = None
        self.title = title
        self._networks: List[Network] = list()

    def create_network(self, name: str):
        network = Network(self, name=name)
        network.save()
        self._networks.append(network)
        return network

    def get_networks(self):
        return self._networks

    def _extend_networks(self, networks_db: List[NetworkDB]):
        for network_db in networks_db:
            network = Network(self, name=network_db.name, network_id=network_db.id)
            self._networks.append(network)

    def create_question(self, text: str):
        """Add question shortcut"""
        network = self.get_networks()[0]
        return network.create_question(text)

    def create_answer(self, text: str):
        """Add answer shortcut"""
        network = self.get_networks()[0]
        return network.create_answer(text)

    def save(self):
        """Save Quest to database"""
        save_object = self.db_object(title=self.title)
        with self.session() as session:
            session.add(save_object)
            session.commit()
            self.id = save_object.id

    def update(self):
        update_object = self.db_object(id=self.id, title=self.title)
        with self.session() as session:
            session.add(update_object)
            session.commit()

    @classmethod
    def load(cls, quest_id: int):
        """Load Quest object from database"""
        with cls.session() as session:
            quest_db = session.query(cls.db_object).filter_by(id=quest_id).one()
            networks_db = quest_db.networks
            quest = cls(quest_db.title)
            quest.id = quest_db.id
            quest._extend_networks(networks_db)
        return quest
