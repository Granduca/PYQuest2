import json
import logging
from jsonschema import Draft7Validator, SchemaError
from flask import current_app
from flask import Blueprint, render_template, session, request

from pref import Preferences
from web.server.rsp import ServerResponse
import web.auth.google.google_auth as google_auth
from web.quest_editor.save_data import save_quest_data, QuestDataError

from sql.database import init_db, engine
from core.user import User

import requests
import os
import pathlib

logging.basicConfig(level=Preferences.logging_level_core)
logger = logging.getLogger(f"{Preferences.app_name} Flask QuestEditor")

bp = Blueprint('quest_editor', __name__, template_folder='templates', static_folder='static')
server_response = ServerResponse()

captcha_secrets_file = os.path.abspath(os.path.join(pathlib.Path(__file__).parent, "../secret/captcha_secret.json"))


class JSONValidateError(ValueError):
    pass


@bp.route('/')
@google_auth.login_is_required
def quest_editor():
    title = Preferences.app_name
    editor_version = '1.0'
    quest_name = 'New Quest 01'

    username = ""
    google_upic = session.get("google_upic", "default_pic.jpg")

    user_id = session.get("user_id")
    if user_id:
        user = User.find(user_id)
        username = user.username

    # check min_js
    min_js = 'false'

    if current_app.config['MIN_JS']:
        min_js = 'true'

    return render_template('quest_editor.html', title=title, editor_version=editor_version, quest_name=quest_name,
                           google_uname=username, google_upic=google_upic, min_js=min_js)


@bp.route('/data', methods=["POST"])
@google_auth.login_is_required
def data_post():
    try:
        data = json.loads(request.data.decode('utf-8'))
        if not validate_json(data):
            raise JSONValidateError("JSON data validation failed")
    except JSONValidateError as e:
        logger.warning(e)
        return server_response.response('error', 'bad_request', msg=e)

    logger.debug(data)
    try:
        init_db(engine)
        user_id = session["user_id"]
        save_quest_data(user_id, data, debug=current_app.config.get("DEBUG"))
    except QuestDataError as e:
        logger.error(e)
        return server_response.internal_server_error(msg=e)
    else:
        return server_response.response('success', 'ok', msg='The quest has been successfully saved')


@bp.route('/captcha', methods=["POST"])
def captcha_post():
    f = open(captcha_secrets_file)
    secret = json.load(f)['server_secret']

    data = {
        'secret': secret,
        'response': request.data
    }

    try:
        response = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data).json()
        if response['success']:
            return server_response.response('success', 'ok', msg=f"Captcha successfully completed at {response['challenge_ts']}")
        else:
            return server_response.response('error', 'forbidden', msg='Captcha not completed')

    except Exception as e:
        logger.error(e)
        return server_response.internal_server_error(msg=e)


def validate_json(data):
    with open('web/quest_editor/schema/schema.json', encoding='utf-8') as f:
        schema = json.load(f)

    try:
        errors = Draft7Validator(schema).iter_errors(data)
    except SchemaError as e:
        logger.error(f' JSON schema error -> {e}')
        return False

    validated = True
    for error in errors:
        logger.warning(f' JSON validation error -> {error.message}')
        validated = False
    return validated
