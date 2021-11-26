from . import node
from pref import Preferences

import logging


logging.basicConfig(level=Preferences.logging_level_core)
logger = logging.getLogger(f"{Preferences.app_name} Question")


class Question(node.GroupNode, node.Node):
    def __init__(self):
        super().__init__()
