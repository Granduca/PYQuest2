from . import node
from pref import Preferences

import logging


logging.basicConfig(level=Preferences.logging_level_core)
logger = logging.getLogger(f"{Preferences.app_name} Answer")


class Answer(node.Node):
    def __init__(self):
        super().__init__()
