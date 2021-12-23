import os
import logging


class Preferences:
    app_name = 'PyQuest2'
    main_db_path = "data/quest.sqlite"
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or f'sqlite:///{main_db_path}'
    logging_level_core = logging.INFO
    logging_level_tools = logging.INFO
