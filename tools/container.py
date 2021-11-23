import core
from pref import Preferences

import logging


logging.basicConfig(level=Preferences.logging_level_tools)
logger = logging.getLogger(f"{Preferences.app_name} Container")


class Container:
    def __init__(self, obj):
        self._obj = obj
        self._data = []

    def add(self, value):
        if value not in self._data:
            self._data.append(value)
        else:
            logger.error(f'\t{value} already exists in the port list')
            return
        if isinstance(value, core.Answer):
            value.in_ports.add(self._obj)

    def remove(self, value):
        if value in self._data:
            self._data.remove(value)
        else:
            logger.error(f'\t{value} was not found in the port list')

    def get(self):
        return self._data
