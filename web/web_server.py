import logging
from flask import Flask
from flask import render_template, redirect, url_for

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


def method_not_allowed(e):
    """Page not found handler"""
    logger.info(e)
    return "ПО ГОЛОВЕ СЕБЕ ПОДЕЛИТЬ", 405


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

    # JS minification
    if app.config['MIN_JS']:
        js_min_generator()

    # Create database directory and file
    create_db()

    # index
    @app.route('/')
    def index():
        return redirect(url_for('auth.index'))

    """ App Handlers """

    # Error handlers
    app.register_error_handler(404, page_not_found)
    app.register_error_handler(405, method_not_allowed)
    app.register_error_handler(500, internal_error)

    """ Blueprints """

    from web.auth.login import bp as login_bp
    from web.auth.google.google_auth import bp as google_bp

    login_bp.register_blueprint(google_bp, url_prefix='/google')
    app.register_blueprint(login_bp, url_prefix='/auth')

    from web.quest_editor.quest_editor import bp as quest_editor_bp
    app.register_blueprint(quest_editor_bp, url_prefix='/quest_editor')

    return app


def js_min_generator():
    import requests
    from pathlib import Path

    routes = {'web/quest_editor/static/': ['workflow.js', 'multiselect.js', 'console.js']}

    for path in routes:
        Path(f"{path}min/").mkdir(parents=True, exist_ok=True)

        for js_file in routes[path]:

            with open(f'{path}{js_file}', 'r', encoding="utf8") as c:
                js = c.read()

            payload = {'input': js}
            url = 'https://www.toptal.com/developers/javascript-minifier/raw'
            logger.debug("Requesting mini-me of {}. . .".format(c.name))
            r = requests.post(url, payload)

            minified = js_file.rstrip('.js') + '.min.js'
            with open(f'{path}min/{minified}', 'w', encoding="utf8") as m:
                m.write(r.text)

            logger.debug("Minification complete. See {}".format(m.name))
