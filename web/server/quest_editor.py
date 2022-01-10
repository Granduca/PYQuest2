import json
import logging
from jsonschema import Draft7Validator
from flask import current_app
from flask import Blueprint, render_template, session, request

from pref import Preferences
from web.server.rsp import ServerResponse
import web.server.google_auth as google_auth
from web.server.save_data import save_quest_data, QuestDataError

from sql.database import init_db, engine
from core.user import User

logging.basicConfig(level=Preferences.logging_level_core)
logger = logging.getLogger(f"{Preferences.app_name} Flask QuestEditor")

bp = Blueprint('quest_editor', __name__)
server_response = ServerResponse()


@bp.route('/quest_editor')
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

    return render_template('quest_editor.html', title=title, editor_version=editor_version, quest_name=quest_name,
                           google_uname=username, google_upic=google_upic)


@bp.route('/quest_editor/data', methods=['GET', 'POST'])
def data_post():
    if request.method == 'GET':
        args = []
        for key in request.args:
            args.append([key, request.args.getlist(key)[0]])
        logger.warning(f"Illegal attempt to get request {args}")
        return render_template('404.html'), 404

    try:
        data = json.loads(request.data.decode('utf-8'))
    except Exception as e:
        # TODO Может только определённые эксшепшены сюда засунуть?
        logger.warning(e)
        return render_template('404.html'), 404
    else:
        if not validate_json(data):
            return server_response.response('error', 'bad_request', msg='JSON data validation failed')

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


def validate_json(data):
    with open('web/schema/schema.json', encoding='utf-8') as f:
        schema = json.load(f)
    try:
        errors = Draft7Validator(schema).iter_errors(data)
    except Exception as e:
        # TODO Может только определённые эксшепшены сюда засунуть?
        logger.warning(f' JSON error -> {e}')
        return False
    validated = True
    for error in errors:
        logger.warning(f' JSON error -> {error.message}')
        validated = False
    return validated
