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

    def __init__(self, title: str):
        self.id = None
        self.title = title
        self._networks = []

    def create_network(self, name: str):
        network = Network(self.id, name=name)
        network.save()
        self._networks.append(network)
        return network

    def extend_networks(self, networks: List[NetworkDB]):
        for network in networks:
            network = Network(self.id, name=network.name, network_id=network.id)
            self._networks.append(network)

    def get_networks(self):
        return self._networks

    def save(self):
        """Save Quest to database"""
        save_object = self.db_object(title=self.title)
        with Session() as session:
            session.add(save_object)
            session.commit()

        self.id = save_object.id

    def update(self):
        update_object = self.db_object(id=self.id, title=self.title)
        with Session() as session:
            session.add(update_object)
            session.commit()

    @classmethod
    def load(cls, quest_id: int):
        """Load Quest object from database"""
        with Session as session:
            quest_db = session.query(cls.db_object).filter_by(id=quest_id).one()
            networks = quest_db.networks
            quest = cls(quest_db.title)
            quest.id = quest_db.id
            quest.extend_networks(networks)
        return quest


""" DEBUG """
if __name__ == "__main__":
    from sql.database import init_db

    def debug():
        title = "Первый квест"
        quest = Quest(title)
        quest.save()

        quest = Quest.load(quest.id)
        assert quest.title == title, "Название квеста не соответствует"
        assert not quest.get_networks(), "У нового квеста существуют сети нод"

    init_db()
    debug()
