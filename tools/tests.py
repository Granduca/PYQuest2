from core import *
from pref import Preferences

import random
import logging


logging.basicConfig(level=Preferences.logging_level_core)
logger = logging.getLogger(f"{Preferences.app_name} Test")


def test_quest_generator(network, max_questions, max_answers_per_question):
    question_default_text = 'Question '
    answer_default_text = 'Answer '

    questions = []
    answers = []

    for i in range(1, 1 + max_questions):
        q = Question()
        q.network = network
        q.text = f'{question_default_text}{i:03d}'
        questions.append(q)

        for j in range(1, 1 + random.randint(1, max_answers_per_question)):
            a = Answer()
            a.network = network
            a.text = f'(Q:{i:03d}) {answer_default_text}{j:03d}'
            q.set_child(a)
            answers.append(a)

    questions_sorter = questions
    questions_sorter = questions_sorter[1:]

    for question in questions:
        for i, answer in enumerate(question.get_childs()):
            if len(question.get_childs()) <= len(questions_sorter):
                answer.set_child(questions_sorter[i])
        questions_sorter = questions_sorter[len(question.get_childs()):]

    # for answer in answers:
    #     for connection in answer.network:
    #         if
    #             answer.is_end = True

    questions[0].get_tree()
