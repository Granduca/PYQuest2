from sql.models import Quest, Network, Node, NodeType, Connection


def test_quest_creation(db_session):
    """Test quest creation and it's modules"""
    # Quest
    quest = Quest(title="Первый квест")
    db_session.add(quest)

    # Network
    network = Network(name="New", quest=quest)
    db_session.add(network)

    # Nodes
    question = Node(network=network, text="Что было раньше?", type=NodeType.question)
    answers = [Node(network=network, text="Курица", type=NodeType.answer),
               Node(network=network, text="Яйцо", type=NodeType.answer)]

    db_session.add(question)
    db_session.add_all(answers)

    # Connection
    connections = [Connection(node_in=question, node_out=answers[0]),
                   Connection(node_in=question, node_out=answers[1])]
    db_session.add_all(connections)

    # Flush all orm objects
    db_session.flush()

    # Tests
    assert quest.id == 1, "Quest id is not 1"
    assert network.id == 1, "Network id is not 1"
    assert question.id == 1, "Node id is not 1"
    assert len(question.connection_out) == 2, "Question doesn't have 2 connections"
    assert len(network.nodes) == 3, "Created 3 nodes"
    assert answers[0].id == 2, "Node id is not 2"
    assert answers[1].id == 3, "Node id is not 3"
