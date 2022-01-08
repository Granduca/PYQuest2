import logging
from flask import Flask

from pref import Preferences
from sql.database import create_db
from .config import ConfigBase, ProductionConfig

logging.basicConfig(level=Preferences.logging_level_core)
logger = logging.getLogger(f"{Preferences.app_name} Flask Server")


def create_app(config: ConfigBase = None):
    """Creating Flask app with specified config"""

    app = Flask(__name__)
    config = config or ProductionConfig
    app.config.from_object(config)

    # Create database directory and file
    create_db()

    from .server.error import bp as error_bp
    app.register_blueprint(error_bp)

    from .server.login import bp as login_bp
    app.register_blueprint(login_bp)

    from .server.google_auth import bp as google_bp
    app.register_blueprint(google_bp)

    from .server.quest_editor import bp as quest_editor_bp
    app.register_blueprint(quest_editor_bp)

    return app
