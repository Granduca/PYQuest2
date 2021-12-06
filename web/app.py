from pref import Preferences

from flask import Flask, render_template, request
import logging


logging.basicConfig(level=Preferences.logging_level_core)
logger = logging.getLogger(f"{Preferences.app_name} Flask")

app = Flask(__name__)


@app.route('/')
def index():
    title = Preferences.app_name
    editor_version = '1.0'
    quest_name = 'New Quest 01'
    return render_template('quest_editor.html', title=title, editor_version=editor_version, quest_name=quest_name)


@app.route('/background_process_test')
def background_process_test():
    print("Hello")
    return "nothing"


@app.route('/data', methods=['GET', 'POST'])
def data_post():
    text = request.data
    logger.info(text)
    return text


if __name__ == '__main__':
    app.run()
