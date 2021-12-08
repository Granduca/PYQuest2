from .node import GroupNode, Node
from pref import Preferences

import logging


logging.basicConfig(level=Preferences.logging_level_core)
logger = logging.getLogger(f"{Preferences.app_name} Question")


class Question(GroupNode):
    def __init__(self):
        super().__init__()
