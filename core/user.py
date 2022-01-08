import logging

from pref import Preferences
from sql.models import User as UserDB


logging.basicConfig(level=Preferences.logging_level_core)
logger = logging.getLogger(f"{Preferences.app_name} User")


class User(UserDB):
    def get_quests(self):
        return self.quests
