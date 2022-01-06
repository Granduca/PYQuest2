from core.node import Node
from pref import Preferences

from sql.models import NodeType

import logging


logging.basicConfig(level=Preferences.logging_level_core)
logger = logging.getLogger(f"{Preferences.app_name} Question")


class Question(Node):
    node_type = NodeType.question

    __mapper_args__ = {'polymorphic_identity': node_type}
