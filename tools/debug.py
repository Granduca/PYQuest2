from core import *
from pref import Preferences

import random
import logging


logging.basicConfig(level=Preferences.logging_level_core)
logger = logging.getLogger(f"{Preferences.app_name} Test")


def debug_quest_generator(quest: Quest, max_questions: int, max_answers_per_question: int):

    logger.info(f"Quest name: \"{quest.title}\"")

    question_default_text = 'Question '
    answer_default_text = 'Answer '

    questions = []
    answers = []

    for i in range(1, 1 + max_questions):
        q = quest.add_question(text=f'{question_default_text}{i:03d}')
        questions.append(q)

        for j in range(1, 1 + random.randint(1, max_answers_per_question)):
            a = quest.add_answer(text=f'(Q:{i:03d}) {answer_default_text}{j:03d}')
            q.set_child(a)
            answers.append(a)

    questions_sorter = questions
    questions_sorter = questions_sorter[1:]

    for question in questions:
        for i, answer in enumerate(question.get_child()):
            if len(question.get_child()) <= len(questions_sorter):
                answer.set_child(questions_sorter[i])
        questions_sorter = questions_sorter[len(question.get_child()):]

    for answer in answers:
        if not answer.get_child():
            answer.set_depth()
            answer.is_end = True

    questions[0].get_tree()
