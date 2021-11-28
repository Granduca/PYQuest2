from . import Network, Question, Answer
from pref import Preferences

import logging


logging.basicConfig(level=Preferences.logging_level_core)
logger = logging.getLogger(f"{Preferences.app_name} Quest")


class Quest:
    def __init__(self, title: str):
        self._title = title
        self._networks = []

    def add_network(self):
        n = Network()
        self._networks.append(n)
        return n

    def add_question(self, **kwargs):
        text = None
        if not self._networks:
            network = self.add_network()
        else:
            network = self._networks[0]
        if 'text' in kwargs:
            text = kwargs['text']
        q = Question()
        q.network = network
        q.text = text
        return q

    def add_answer(self, **kwargs):
        text = None
        if not self._networks:
            network = self.add_network()
        else:
            network = self._networks[0]
        if 'text' in kwargs:
            text = kwargs['text']
        a = Answer()
        a.network = network
        a.text = text
        return a

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, title: str):
        self._title = title
