from core import *

import random


def test_quest_generator(max_questions, max_answers_per_question):
    question_default_text = 'Question '
    answer_default_text = 'Answer '

    questions = []
    answers = []

    for i in range(1, 1 + max_questions):
        q = Question()
        q.text = f'{question_default_text}{i:03d}'
        questions.append(q)

        for j in range(1, 1 + random.randint(1, max_answers_per_question)):
            a = Answer()
            a.text = f'(Q:{i:03d}) {answer_default_text}{j:03d}'
            q.out_ports.add(a)
            answers.append(a)

    questions_sorter = questions
    questions_sorter = questions_sorter[1:]

    for question in questions:
        for i, answer in enumerate(question.out_ports.get()):
            if len(question.out_ports.get()) <= len(questions_sorter):
                answer.out_ports.add(questions_sorter[i])
        questions_sorter = questions_sorter[len(question.out_ports.get()):]

    for answer in answers:
        if not answer.out_ports.get():
            answer.is_end = True

    questions[0].get_tree()