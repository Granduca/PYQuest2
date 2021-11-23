from tools import Container
from pref import Preferences

import logging
import uuid


logging.basicConfig(level=Preferences.logging_level_core)
logger = logging.getLogger(f"{Preferences.app_name} Node")


class Node:
    def __init__(self):
        self._id = uuid.uuid4()     # TODO заменить на id с SQL
        self.in_ports = Container(self)
        self.out_ports = Container(self)
        self._text = ''
        self.is_start = False
        self.is_end = False

    @property
    def id(self):
        logger.info(f"\tNode id is '{self._id}'")
        return self._id

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, text):
        self._text = text
        logger.info(f"\tText set as '{text}'")

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

        if self.out_ports:
            for port in self.out_ports.get():
                if not self.is_end:
                    if port != node_from:
                        port.get_tree(node_from=node_from, depth=depth+1, divider=divider)
                    else:
                        logger.info(f"TREE:{divider*(depth+1)}<--")
                else:
                    logger.info(f"TREE:{divider * (depth+1)}END")
