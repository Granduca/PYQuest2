import pytest


@pytest.fixture()
def memory_session():
    # SetUp
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    memory_engine = create_engine("sqlite:///:memory:", echo=True)
    session = sessionmaker(bind=memory_engine)

    from sql.database import init_db
    init_db(_engine=memory_engine)
    return session


@pytest.fixture
def db_session():
    # SetUp
    from sql.database import Session, init_db

    # Create database
    init_db()

    with Session.begin() as session:
        yield session

        # Teardown
        session.rollback()
