from core import Quest, Network, Node, Connection, Answer, Question


def test_quest(mem_session_maker):
    """Quest creation"""

    title = "Первый квест"
    quest = Quest(title)

    # SetUp
    Quest.session = mem_session_maker
    Network.session = mem_session_maker
    Node.session = mem_session_maker
    Connection.session = mem_session_maker

    quest.save()

    quest = Quest.load(quest.id)
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

    network = Network.load(quest, network.id)
    assert network.id == 1
    question = Question.load(network, question.id)
    answer = Answer.load(network, answer.id)
    assert question.id == 1
    assert answer.id == 2

    network.create_connection(question, answer)
