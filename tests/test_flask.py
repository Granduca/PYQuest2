import pytest
from web.web_server import create_app


def response_text(data: bytes):
    return data.decode("utf-8")


def google_log_in(client):
    with client.session_transaction() as sess:
        sess["google_id"] = "test_id"
        sess["google_uname"] = "Tester"
        sess["google_upic"] = "picture"
    return client


def google_log_out(client):
    client.get("google/logout")
    return client


@pytest.fixture()
def flask_client():
    flask_app = create_app()

    # Create a test client using the Flask application configured for testing
    with flask_app.test_client() as testing_client:
        # Establish an application context
        with flask_app.app_context():
            yield testing_client  # this is where the testing happens!


@pytest.fixture()
def flask_google_client(flask_client):
    return google_log_in(flask_client)


class TestNotLogin:
    def test_index(self, flask_client):
        response = flask_client.get('/')
        assert response.status_code == 200
        r_text = response_text(response.data)
        assert "Войти через социальные сети" in r_text

    def test_quest_editor_redirect(self, flask_client):
        response = flask_client.get('/quest_editor')
        assert response.status_code == 302
        assert "index" in response.location
        assert "?login_is_required=true" in response.location

    def test_quest_editor_redirection(self, flask_client):
        response = flask_client.get('/quest_editor', follow_redirects=True)
        assert response.status_code == 200
        r_text = response_text(response.data)
        assert "Сначала нужно выполнить вход!" in r_text


class TestLogin:
    def test_log_in(self, flask_client):
        flask_logged_client = google_log_in(flask_client)
        with flask_logged_client.session_transaction() as session:
            assert session.get("google_id") == "test_id"
            assert session.get("google_uname") == "Tester"
            assert session.get("google_upic") == "picture"

    def test_log_out(self, flask_client):
        flask_logged_client = google_log_in(flask_client)
        flask_logged_out_client = google_log_out(flask_logged_client)
        with flask_logged_out_client.session_transaction() as session:
            assert not session

    def test_index_redirection(self, flask_google_client):
        response = flask_google_client.get('/', follow_redirects=True)
        assert response.status_code == 200
        r_text = response_text(response.data)
        assert "PyQuest2 | Quest Editor" in r_text
