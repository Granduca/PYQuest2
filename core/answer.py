from .node import Node
from pref import Preferences

from sql.models import NodeType

import logging


logging.basicConfig(level=Preferences.logging_level_core)
logger = logging.getLogger(f"{Preferences.app_name} Answer")


class Answer(Node):
    type = NodeType.answer

    def __init__(self, network, answer: str):
        super().__init__(network, answer)
