from pref import Preferences

from core.network import Network

from sql.models import Quest as QuestDB

import logging

logging.basicConfig(level=Preferences.logging_level_core)
logger = logging.getLogger(f"{Preferences.app_name} Quest")


class Quest(QuestDB):
    def get_networks(self):
        return Network.query.filter_by(quest_id=self.id).all()

    def create_network(self, name: str):
        network = Network.create(quest_id=self.id, name=name)
        network.save()
        return network

    def create_question(self, text: str):
        """Add question shortcut"""
        network = self.get_networks()[0]
        return network.create_question(text)

    def create_answer(self, text: str):
        """Add answer shortcut"""
        network = self.get_networks()[0]
        return network.create_answer(text)
