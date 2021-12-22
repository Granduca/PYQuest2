from pref import Preferences
from core import *

from flask import Flask, render_template, request
import json
import logging


logging.basicConfig(level=Preferences.logging_level_core)
logger = logging.getLogger(f"{Preferences.app_name} Flask")

app = Flask(f"{Preferences.app_name} Editor")


@app.route('/')
def index():
    """Main page"""
    title = Preferences.app_name
    editor_version = '1.0'
    quest_name = 'New Quest 01'
    return render_template('quest_editor.html', title=title, editor_version=editor_version, quest_name=quest_name)


@app.route('/data', methods=['GET', 'POST'])
def data_post():
    data = json.loads(request.data.decode('utf-8'))
    # logger.info(data)
    quest = Quest('Test Quest 01')
    questions = []
    answers = []

    for node in data['drawflow']['Home']['data'].values():
        if node['class'] == 'question':
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

        if node['class'] == 'answer':
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

    first.get_tree()

    return "ok"


@app.post('/save')
def save_quest():
    """
    Validate and saves data to database
    """
    data = json.loads(request.data.decode('utf-8'))
    logger.debug(f"Saving quest with: {data}")

    return "ok"


if __name__ == '__main__':
    app.run()
