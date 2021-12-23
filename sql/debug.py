

if __name__ == "__main__":
    """ Test database creation """
    from sql.database import Session, init_db

    # Create database
    init_db()
    # Base.metadata.create_all(engine)

    from sql.models import Quest, Network, Node, NodeType, Connection

    with Session.begin() as session:
        # Open session transaction

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

        # Print out
        print(quest)
        print(network)
        print(network.nodes)
        print(question.connection_out)
        print(connections)

        # Tests
        assert quest.id == 1, "Quest id is not 1"
        assert network.id == 1, "Network id is not 1"
        assert question.id == 1, "Node id is not 1"
        assert len(question.connection_out) == 2, "Question doesn't have 2 connections"
        assert answers[0].id == 2, "Node id is not 2"
        assert answers[1].id == 3, "Node id is not 3"

        # Rollback tests
        session.rollback()
