from core import Quest, Answer, Question


def test_user(user):
    assert user.id == 1


def test_simple_quest(session, user):
    """Quest creation"""

    # SetUp
    # Quest.set_session(session)

    title = "Первый квест"
    quest = Quest.create(owner_id=user.id, title=title)

    quest = Quest.find(quest.id)
    assert quest.title == title, "Название квеста не соответствует"
    # assert not quest.get_nodes(), "У нового квеста существуют ноды"

    question = quest.create_question("Вопрос")
    assert question.text == "Вопрос"
    answer = quest.create_answer("Ответ")
    assert answer.text == "Ответ"

    quest_nodes = quest.get_nodes()
    assert len(quest_nodes) == 2

    connection = quest.connect_nodes(question, answer)
    assert connection.node_out
    assert connection.node_in

    quest = Quest.find(quest.id)
    assert quest.id == 1
    assert len(quest.get_nodes()) == 2
    question = Question.find(question.id)
    answer = Answer.find(answer.id)
    assert question.id == 1
    assert answer.id == 2


def test_complex_quest(session, user):
    title = "Первый квест"
    quest = Quest.create(owner_id=user.id, title=title)

    first_question = quest.create_question("Что было раньше?")
    first_answers = list()
    first_answers.append(quest.create_answer("Курица"))
    first_answers.append(quest.create_answer("Яйцо"))
    for answer in first_answers:
        quest.connect_nodes(first_question, answer)

    second_question = quest.create_question("Она вкусная?")
    quest.connect_nodes(first_answers[0], second_question)
    second_answers = list()
    second_answers.append(quest.create_answer("Да"))
    second_answers.append(quest.create_answer("Нет"))
    second_answers.append(quest.create_answer("Сочная"))
    for answer in second_answers:
        quest.connect_nodes(second_question, answer)

    assert len(quest.get_nodes()) == 7
    assert len(quest.get_starts()) == 1
    assert len(quest.get_ends()) == 4
