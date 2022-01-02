from .node import Node
from pref import Preferences

from sql.models import NodeType

import logging


logging.basicConfig(level=Preferences.logging_level_core)
logger = logging.getLogger(f"{Preferences.app_name} Question")


class Question(Node):
    type = NodeType.question

    def __init__(self, network, question: str):
        super().__init__(network, question)
