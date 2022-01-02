from sql.models import Quest, Network, Node, NodeCoordinates, NodeType, Connection


def test_session_maker_fixture(mem_session_maker):
    """Test session maker for memory bind and models"""
    session = mem_session_maker()
    bind = session.get_bind()
    assert not bind.url.database or bind.url.database == ":memory:", "Session is not :memory: type"

    # Models imported
    assert len(bind.table_names()) > 0
    models = Quest, Network, Node, Connection, NodeCoordinates
    assert set(bind.table_names()) == {table.__tablename__ for table in models}


def test_session_fixture(session):
    """Test session for memory bind"""
    bind = session.get_bind()
    assert not bind.url.database or bind.url.database == ":memory:", "Session is not :memory: type"


def test_quest_creation(session):
    """Test quest creation and it's relations"""
    # Quest
    quest = Quest(title="Первый квест")
    session.add(quest)

    # Network
    network = Network(name="New", quest=quest)
    session.add(network)

    # Nodes
    question = Node(network=network, text="Что было раньше?", type=NodeType.question)
    answers = [Node(network=network, text="Курица", type=NodeType.answer),
               Node(network=network, text="Яйцо", type=NodeType.answer)]

    session.add(question)
    session.add_all(answers)

    # Connection
    connections = [Connection(node_in=question, node_out=answers[0]),
                   Connection(node_in=question, node_out=answers[1])]
    session.add_all(connections)

    # Flush all orm objects
    session.flush()

    # Tests
    assert quest.id == 1, "Quest id is not 1"
    assert network.id == 1, "Network id is not 1"
    assert question.id == 1, "Node id is not 1"
    assert len(question.connections_out) == 2, "Question doesn't have 2 connections"
    assert len(network.nodes) == 3, "Created 3 nodes"
    assert len(answers[0].connections_in) == 1
    assert len(answers[1].connections_in) == 1
    assert answers[0].id == 2, "Node id is not 2"
    assert answers[1].id == 3, "Node id is not 3"
