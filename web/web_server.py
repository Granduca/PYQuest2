from pref import Preferences
from core import *
from web.server.rsp import ServerResponse

from flask import Flask, render_template, request, session, abort, redirect, request
from jsonschema import Draft7Validator
import json
import logging

import os
import pathlib
from functools import wraps

import requests
from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow
from pip._vendor import cachecontrol
import google.auth.transport.requests


logging.basicConfig(level=Preferences.logging_level_core)
logger = logging.getLogger(f"{Preferences.app_name} Flask")

app = Flask(f"{Preferences.app_name} Editor")
app.secret_key = "PyQuest2"
server_response = ServerResponse()

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

client_secrets_file = os.path.join(pathlib.Path(__file__).parent, "secret/client_secret.json")

flow = Flow.from_client_secrets_file(
    client_secrets_file=client_secrets_file,
    scopes=["https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email", "openid"],
    redirect_uri="http://127.0.0.1:5000/callback"
)


def login_is_required(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        if "google_id" not in session:
            return redirect("/")  # Authorization required
        else:
            return function()

    return wrapper


@app.route('/')
def index():
    title = Preferences.app_name
    editor_version = '1.0'
    return render_template('index.html', title=title, editor_version=editor_version)


@app.route('/quest_editor')
@login_is_required
def quest_editor():
    title = Preferences.app_name
    editor_version = '1.0'
    quest_name = 'New Quest 01'
    if session:
        if 'google_uname' in session and 'google_upic' in session:
            google_uname = session['google_uname']
            google_upic = session['google_upic']
        else:
            google_uname = ""
            google_upic = ""
    else:
        google_uname = ""
        google_upic = ""
    return render_template('quest_editor.html', title=title, editor_version=editor_version, quest_name=quest_name, google_uname=google_uname, google_upic=google_upic)


@app.route('/data', methods=['GET', 'POST'])
def data_post():
    data = json.loads(request.data.decode('utf-8'))

    if not validate_json(data):
        return server_response.response('error', 'bad_request', msg='JSON data validation failed')

    # logger.info(data)
    quest = Quest(data['quest'])
    questions = []
    answers = []

    node_types = {
        "question": ['question', 'question_not_connected', 'start'],
        "answer": ['answer', 'answer_not_connected', 'finish', 'link']
    }

    first = None

    max_text_length = 4000  # В телеграме ограничение 4096 символов на сообщение

    for node in data['nodes']:
        if node['class'] not in node_types['question'] and node['class'] not in node_types['answer']:
            return server_response.internal_server_error(msg="Bad node type")
        if node['class'] in node_types['question']:
            inputs = []
            outputs = []
            text = node['data']

            if len(text) > max_text_length:
                return server_response.internal_server_error(msg="The maximum permissible text length has been exceeded")

            q = quest.add_question(text=node['data'])
            q.id = node['id']

            if node['connections']['input']:
                for connection in node['connections']['input']:
                    inputs.append((connection['node'], node['id']))

            if node['connections']['output']:
                for connection in node['connections']['output']:
                    outputs.append((node['id'], connection['node']))
            question = {
                'node': q,
                'inputs': inputs,
                'outputs': outputs,
            }
            questions.append(question)
            if node['class'] == 'start':
                first = question['node']

        if node['class'] in node_types['answer']:
            inputs = []
            outputs = []
            if node['class'] != 'link':
                text = node['data']
            else:
                text = f"LINK: {node['link']}"  # для дебага

            if len(text) > max_text_length:
                return server_response.internal_server_error(msg="The maximum permissible text length has been exceeded")

            a = quest.add_answer(text=text)
            a.id = node['id']

            if node['connections']['input']:
                for connection in node['connections']['input']:
                    inputs.append((connection['node'], node['id']))

            if node['connections']['output']:
                for connection in node['connections']['output']:
                    outputs.append((node['id'], connection['node']))
            answer = {
                'node': a,
                'inputs': inputs,
                'outputs': outputs,
            }
            answers.append(answer)
            if node['class'] == 'finish' or node['class'] == 'link':
                answer['node'].is_end = True
            # в будущем линки надо отдельно обрабатывать

    for item in questions:
        if item['outputs']:
            for i in item['outputs']:
                for a in answers:
                    if a['node'].id == i[1]:
                        item['node'].set_child(a['node'])

    for item in answers:
        if item['outputs']:
            for i in item['outputs']:
                for q in questions:
                    if q['node'].id == i[1]:
                        item['node'].set_child(q['node'])

    for answer in answers:
        if not answer['node'].get_child():
            answer['node'].set_depth()
            answer['node'].is_end = True

    if not first:
        for question in questions:
            if not question['inputs']:
                first = question['node']

    if first:
        first.get_tree()
    else:
        return server_response.internal_server_error(msg="Failed to assign start node")

    return server_response.response('success', 'ok', msg='The quest has been successfully saved')


@app.route("/login")
def login():
    authorization_url, state = flow.authorization_url()
    session["state"] = state
    return redirect(authorization_url)


@app.route("/callback")
def callback():
    flow.fetch_token(authorization_response=request.url)

    if not session["state"] == request.args["state"]:
        abort(500)  # State does not match!

    credentials = flow.credentials
    request_session = requests.session()
    cached_session = cachecontrol.CacheControl(request_session)
    token_request = google.auth.transport.requests.Request(session=cached_session)
    with open(client_secrets_file, encoding='utf-8') as f:
        client_id = json.load(f)['web']['client_id']

    id_info = id_token.verify_oauth2_token(
        id_token=credentials._id_token,
        request=token_request,
        audience=client_id
    )

    session["google_id"] = id_info.get("sub")
    session["google_uname"] = id_info.get("name")
    session["google_upic"] = id_info.get("picture")
    return redirect("/quest_editor")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def page_not_found(e):
    return render_template('404.html'), 500


def validate_json(data):
    with open('schema/schema.json', encoding='utf-8') as f:
        schema = json.load(f)
    try:
        errors = Draft7Validator(schema).iter_errors(data)
    except Exception as e:
        logger.warning(f' JSON error -> {e}')
        return False
    validated = True
    for error in errors:
        logger.warning(f' JSON error -> {error.message}')
        validated = False
    return validated


if __name__ == '__main__':
    app.run()
