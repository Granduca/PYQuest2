import logging
from flask import Flask
from flask import render_template, redirect

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

    # index
    @app.route('/')
    def index():
        return redirect('/auth')

    """ App Handlers """

    # Error handlers
    app.register_error_handler(404, page_not_found)
    app.register_error_handler(500, internal_error)

    """ Blueprints """

    from web.auth.login import bp as login_bp
    from web.auth.google.google_auth import bp as google_bp

    login_bp.register_blueprint(google_bp, url_prefix='/google')
    app.register_blueprint(login_bp, url_prefix='/auth')

    from web.quest_editor.quest_editor import bp as quest_editor_bp
    app.register_blueprint(quest_editor_bp, url_prefix='/quest_editor')

    return app
