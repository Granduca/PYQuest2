from pref import Preferences

from sql.models import Node as NodeDB

import logging


logging.basicConfig(level=Preferences.logging_level_core)
logger = logging.getLogger(f"{Preferences.app_name} Node")


class Node(NodeDB):
    pass
