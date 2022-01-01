import pytest


@pytest.fixture()
def mem_session_maker():
    """Represents session maker with memory engine bind"""
    # SetUp
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    memory_engine = create_engine("sqlite:///")
    session = sessionmaker(bind=memory_engine)

    from sql.database import init_db
    init_db(_engine=memory_engine)
    return session


@pytest.fixture
def session(mem_session_maker):
    """Create session and roll it back on teardown"""

    # SetUp
    with mem_session_maker.begin() as session:

        # Use session fixture
        yield session

        # Teardown
        session.rollback()
