from sql.models import User, Quest, Node, NodeAttributes, NodeType, Connection


def test_session_maker_fixture(mem_session_maker):
    """Test session maker for memory bind and models"""
    session = mem_session_maker()
    bind = session.get_bind()
    assert not bind.url.database or bind.url.database == ":memory:", "Session is not :memory: type"

    # Models imported
    assert len(bind.table_names()) > 0
    models = User, Quest, Node, Connection, NodeAttributes
    assert set(bind.table_names()) == {table.__tablename__ for table in models}


def test_session_fixture(session):
    """Test session for memory bind"""
    bind = session.get_bind()
    assert not bind.url.database or bind.url.database == ":memory:", "Session is not :memory: type"


def test_quest_creation(session, user):
    """Test quest creation and it's relations"""
    # Quest
    Quest.set_session(session)

    quest = Quest.create(owner_id=user.id, title="Первый квест")

    assert not quest.nodes

    # Nodes
    question = Node.create(quest=quest, text="Что было раньше?", type=NodeType.question)
    answers = [Node.create(quest=quest, text="Курица", type=NodeType.answer),
               Node.create(quest=quest, text="Яйцо", type=NodeType.answer)]

    # Connection
    connections = [Connection.create(node_in=question, node_out=answers[0]),
                   Connection.create(node_in=question, node_out=answers[1])]

    # Tests
    assert quest.id == 1, "Quest id is not 1"
    assert question.id == 1, "Node id is not 1"
    assert len(question.connections_out) == 2, "Question doesn't have 2 connections"
    assert len(quest.nodes) == 3, "Created 3 nodes"
    assert len(answers[0].connections_in) == 1
    assert len(answers[1].connections_in) == 1
    assert answers[0].id == 2, "Node id is not 2"
    assert answers[1].id == 3, "Node id is not 3"
