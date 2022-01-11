import json

export = {"drawflow": {"Home": {"data": {}}}}
node = {
    "id": 0,
    "name": "question_not_connected",
    "data": {
        "template": ""
    },
    "class": "question_not_connected",
    "html": "<div><div class=\"title-box not_connected noselect\" ondblclick=\"set_start(event)\"><i class=\"fas fa-question-circle\"></i> Вопрос</div><div class=\"box noselect\"><textarea df-template class=\"vertical\" style=\"height:100px;\" placeholder=\"Введите ваш текст...\"></textarea></div></div>",
    "typenode": False,
    "inputs": {"input_1": {"connections": []}},
    "outputs": {"output_1": {"connections": []}},
    "pos_x": float(150),
    "pos_y": float(150)
}


def main():
    step = 0
    offset = 10
    width = 100
    start_offset = 150
    for i in range(0, 500):
        n = dict()
        n['id'] = i
        n['name'] = node['name']
        n['data'] = node['data']
        n['class'] = node['class']
        n['html'] = node['html']
        n['typenode'] = node['typenode']
        n['inputs'] = node['inputs']
        n['outputs'] = node['outputs']
        if i % width == 0:
            step += 1
        n['pos_x'] = float((start_offset + (offset * width)) + (offset * i) - (offset * width * step))
        n['pos_y'] = float(start_offset + offset * step * 0)
        export['drawflow']['Home']['data'][str(i)] = n

    with open('test_nodes.json', 'w') as file:
        file.write(json.dumps(export))


if __name__ == "__main__":
    main()
