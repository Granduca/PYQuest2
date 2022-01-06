from .node import Node
from pref import Preferences

from sql.models import NodeType

import logging


logging.basicConfig(level=Preferences.logging_level_core)
logger = logging.getLogger(f"{Preferences.app_name} Answer")


class Answer(Node):
    node_type = NodeType.answer

    __mapper_args__ = {'polymorphic_identity': node_type}
