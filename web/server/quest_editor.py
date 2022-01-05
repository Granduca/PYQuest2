from pref import Preferences
from core import *
from web.server.rsp import ServerResponse
import web.server.google_auth as google_auth

from flask import Blueprint, render_template, session, request
from jsonschema import Draft7Validator
import json
import logging

logging.basicConfig(level=Preferences.logging_level_core)
logger = logging.getLogger(f"{Preferences.app_name} Flask QuestEditor")

app = Blueprint('quest_editor', f"{Preferences.app_name} Editor")
server_response = ServerResponse()


@app.route('/quest_editor')
@google_auth.login_is_required
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


@app.route('/quest_editor/data', methods=['GET', 'POST'])
def data_post():
    # TODO: добавить сессию
    if request.method == 'GET':
        args = []
        for key in request.args:
            args.append([key, request.args.getlist(key)[0]])
        logger.warning(f"Illegal attempt to get request {args}")
        return render_template('404.html'), 404

    if request.method != 'POST':
        return render_template('404.html'), 404

    try:
        data = json.loads(request.data.decode('utf-8'))
    except Exception as e:
        logger.warning(e)
        return render_template('404.html'), 404

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

            if len(f'{text}') > max_text_length:
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

            if len(f'{text}') > max_text_length:
                return server_response.internal_server_error(msg="The maximum permissible text length has been exceeded")

            a = quest.add_answer(text=text)
            a.id = node['id']

            if node['connections']['input']:
                for connection in node['connections']['input']:
                    inputs.append((connection['node'], node['id']))

            if node['connections']['output']:
                for connection in node['connections']['output']:
                    outputs.append((node['id'], connection['node']))

            if node['class'] == 'link':
                outputs.append((node['id'], node['link']))

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
