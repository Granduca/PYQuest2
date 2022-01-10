import logging
from flask import Flask
from flask import render_template

from pref import Preferences
from sql.database import create_db
from .config import ConfigBase, ProductionConfig

logging.basicConfig(level=Preferences.logging_level_core)
logger = logging.getLogger(f"{Preferences.app_name} Flask Server")


""" Error handlers """


def page_not_found(e):
    """Page not found handler"""
    logger.info(e)
    return render_template("404.html"), 404


def internal_error(e):
    """Internal error handler"""
    logger.info(e)
    return render_template("500.html"), 500


def create_app(config: ConfigBase = None):
    """
    Creating Flask app with specified config
    :param config: Configuration class from config.py or specify with FLASK_ENV
    """

    app = Flask(__name__)
    config = config or ProductionConfig
    app.config.from_object(config)

    # Create database directory and file
    create_db()

    """ App Handlers """

    # Error handlers
    app.register_error_handler(404, page_not_found)
    app.register_error_handler(500, internal_error)

    """ Blueprints """

    from .server.login import bp as login_bp
    app.register_blueprint(login_bp)

    from .server.google_auth import bp as google_bp
    app.register_blueprint(google_bp)

    from .server.quest_editor import bp as quest_editor_bp
    app.register_blueprint(quest_editor_bp)

    return app
