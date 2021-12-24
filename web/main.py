from pref import Preferences
from core import *
from web.server.rsp import ServerResponse

from flask import Flask, render_template, request
from jsonschema import Draft7Validator
import json
import logging


logging.basicConfig(level=Preferences.logging_level_core)
logger = logging.getLogger(f"{Preferences.app_name} Flask")

app = Flask(f"{Preferences.app_name} Editor")
server_response = ServerResponse()


@app.route('/')
def index():
    title = Preferences.app_name
    editor_version = '1.0'
    quest_name = 'New Quest 01'
    return render_template('quest_editor.html', title=title, editor_version=editor_version, quest_name=quest_name)
    # return render_template('index.html', title=title, editor_version=editor_version)


@app.route('/data', methods=['GET', 'POST'])
def data_post():
    data = json.loads(request.data.decode('utf-8'))

    if not validate_json(data):
        return server_response.response('error', 'bad_request', msg='JSON data validation failed')

    # logger.info(data)
    quest = Quest('Test Quest 01')
    questions = []
    answers = []

    for node in data['drawflow']['Home']['data'].values():
        if node['class'] == 'question' or node['class'] == 'question_not_connected':
            inputs = []
            outputs = []
            q = quest.add_question(text=node['data']['template'])
            q.id = int(node['id'])

            if node['inputs']['input_1']['connections']:
                for connection in node['inputs']['input_1']['connections']:
                    inputs.append((int(connection['node']), int(node['id'])))

            if node['outputs']['output_1']['connections']:
                for connection in node['outputs']['output_1']['connections']:
                    outputs.append((int(node['id']), int(connection['node'])))
            question = {
                'node': q,
                'inputs': inputs,
                'outputs': outputs,
            }
            questions.append(question)

        if node['class'] == 'answer' or node['class'] == 'answers_not_connected':
            inputs = []
            outputs = []
            a = quest.add_answer(text=node['data']['template'])
            a.id = int(node['id'])

            if node['inputs']['input_1']['connections']:
                for connection in node['inputs']['input_1']['connections']:
                    inputs.append((int(connection['node']), int(node['id'])))

            if node['outputs']['output_1']['connections']:
                for connection in node['outputs']['output_1']['connections']:
                    outputs.append((int(node['id']), int(connection['node'])))
            answer = {
                'node': a,
                'inputs': inputs,
                'outputs': outputs,
            }
            answers.append(answer)

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

    first = None
    for question in questions:
        if not question['inputs']:
            first = question['node']

    if first:
        first.get_tree()
    else:
        return server_response.internal_server_error(msg="Failed to assign start node")

    return server_response.response('success', 'ok', msg='The quest has been successfully saved')


def validate_json(data):
    with open('schema.json', encoding='utf-8') as f:
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
