from pref import Preferences
import server.google_auth as google_auth
import server.quest_editor as quest_editor

from flask import Flask, render_template, request
import logging

logging.basicConfig(level=Preferences.logging_level_core)
logger = logging.getLogger(f"{Preferences.app_name} Flask")

app = Flask(f"{Preferences.app_name} Editor")
app.secret_key = "PyQuest2"

app.register_blueprint(google_auth.app)
app.register_blueprint(quest_editor.app)


@app.route('/', methods=['GET'])
def index():
    login_is_required = ''
    if "login_is_required" in request.args:
        login_is_required = request.args['login_is_required']
    title = Preferences.app_name
    editor_version = '1.0'
    return render_template('index.html', title=title, editor_version=editor_version, login_is_required=login_is_required)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def page_not_found(e):
    return render_template('404.html'), 500


if __name__ == '__main__':
    app.run()
