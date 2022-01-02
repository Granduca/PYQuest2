from core import Quest, Network, Answer, Question


def test_quest(session):
    """Quest creation"""

    # SetUp
    Quest.set_session(session)

    title = "Первый квест"
    quest = Quest.create(title=title)

    quest.save()

    quest = Quest.find(quest.id)
    assert quest.title == title, "Название квеста не соответствует"
    assert not quest.get_networks(), "У нового квеста существуют сети нод"

    network = quest.create_network("First")
    assert quest.get_networks()

    question = quest.create_question("Вопрос")
    assert question.text == "Вопрос"
    answer = quest.create_answer("Ответ")
    assert answer.text == "Ответ"

    network_nodes = network.get_nodes()
    assert len(network_nodes) == 2

    network = Network.find(network.id)
    assert network.id == 1
    question = Question.find(question.id)
    answer = Answer.find(answer.id)
    assert question.id == 1
    assert answer.id == 2
