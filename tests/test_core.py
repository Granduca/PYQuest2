from core import Quest, Answer, Question


def test_quest(session):
    """Quest creation"""

    # SetUp
    Quest.set_session(session)

    title = "Первый квест"
    quest = Quest.create(title=title)

    quest.save()

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
