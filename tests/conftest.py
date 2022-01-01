import pytest


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
