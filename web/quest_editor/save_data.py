from collections import defaultdict
from typing import List, Dict

from core import Quest
from core import User
from core import Node


class QuestDataError(ValueError):
    """Quest data is invalid"""
    pass


def save_quest_data(user_id: int, data: dict, debug: bool = False):
    """
    Saves all data of quest from json
    :param: json request -> data
    :raise: QuestDataError on invalid data
    :return: None
    """
    node_types = {
        "question": ['question', 'question_not_connected', 'start'],
        "answer": ['answer', 'answer_not_connected', 'finish', 'link']
    }
    max_text_length = 4096  # В телеграм ограничение 4096 символов на сообщение

    # Create quest object
    quest_name = data["quest"]
    quest = Quest.create(owner_id=user_id, title=quest_name)

    nodes = data['nodes']
    node_object: Dict[int, Node] = dict()  # Link front-end objects to back-end objects
    node_connections: Dict[int, List[int]] = defaultdict(list)
    for node in nodes:
        node_id = node['id']
        node_type = node["class"]
        text = node['data']
        output_connections = node["connections"]["output"]

        # if node['class'] == "link":
        #     text = f"LINK: {node['link']}"

        if len(text) > max_text_length:
            raise QuestDataError("The maximum permissible text length has been exceeded")

        # Question creation
        if node_type in node_types['question']:
            node_obj = quest.create_question(text=text)

        # Answer creation
        elif node_type in node_types['answer']:
            node_obj = quest.create_answer(text=text)
        else:
            raise QuestDataError("Bad node type")

        # Link front-end object to back-end
        node_object[node_id] = node_obj

        if output_connections:
            for connection in output_connections:
                connected_node_id = connection["node"]
                node_connections[node_id].append(connected_node_id)

    for node_id, node_obj in node_object.items():
        for connected_id in node_connections[node_id]:
            connected_node = node_object[connected_id]
            node_obj.set_child(connected_node)

    if debug:
        quest.show_debug_tree()

    return


def get_user_quests(user_id: int):
    if not isinstance(user_id, int):
        raise TypeError(f"User id must be int, got: {type(user_id)} {user_id}")
    user = User.find(user_id)
    user_quests = user.get_quests()
    return {"user": user, "quests": user_quests}


def get_quest_data(quest_id: int):
    if not isinstance(quest_id, int):
        raise TypeError(f"Quest id must be int, got: {type(quest_id)} {quest_id}")

    quest = Quest.find(quest_id)
    quest_nodes = quest.get_nodes()
    quest_connections = quest.get_connections()
    return {"quest": quest, "nodes": quest_nodes, "connections": quest_connections}
