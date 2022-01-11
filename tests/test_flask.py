import pytest


def response_text(data: bytes):
    return data.decode("utf-8")


def google_log_in(client):
    with client.session_transaction() as sess:
        sess["user_id"] = 1
        sess["google_upic"] = "picture"
    return client


def google_log_out(client):
    client.get("auth/google/logout")
    return client


@pytest.fixture(scope="class")
def flask_client():
    from web.web_server import create_app
    flask_app = create_app()

    # Create a test client using the Flask application configured for testing
    with flask_app.test_client() as testing_client:
        # Establish an application context
        with flask_app.app_context():
            yield testing_client  # this is where the testing happens!


@pytest.fixture
def flask_google_client(flask_client, user):
    return google_log_in(flask_client)


class TestNotLogin:
    def test_index(self, flask_client):
        response = flask_client.get('/')
        assert response.status_code == 302
        assert "auth" in response.location

    def test_index_redirect(self, flask_client):
        response = flask_client.get('/', follow_redirects=True)
        assert response.status_code == 200
        r_text = response_text(response.data)
        assert "Войти через социальные сети" in r_text

    def test_auth(self, flask_client):
        response = flask_client.get('/auth/')
        assert response.status_code == 200
        r_text = response_text(response.data)
        assert "Войти через социальные сети" in r_text

    def test_quest_editor_redirect(self, flask_client):
        response = flask_client.get('/quest_editor/')
        assert response.status_code == 302
        assert "auth" in response.location
        assert "?login_is_required=true" in response.location

    def test_quest_editor_redirect_delete(self, flask_client):
        response = flask_client.delete('/quest_editor/')
        assert response.status_code == 405
        assert response_text(response.data) == "ПО ГОЛОВЕ СЕБЕ ПОДЕЛИТЬ"

    def test_quest_editor_redirection(self, flask_client):
        response = flask_client.get('/quest_editor/', follow_redirects=True)
        assert response.status_code == 200
        r_text = response_text(response.data)
        assert "Сначала нужно выполнить вход!" in r_text

    def test_quest_editor_data_post(self, flask_client, json_request):
        import json
        response = flask_client.post('/quest_editor/data', data=json.dumps(json_request))
        assert response.status_code == 302


class TestLogin:
    def test_log_in(self, flask_client):
        flask_logged_client = google_log_in(flask_client)
        with flask_logged_client.session_transaction() as session:
            assert session.get("user_id") == 1
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

    def test_quest_editor_data_post(self, flask_google_client, json_request):
        import json
        response = flask_google_client.post('/quest_editor/data', data=json.dumps(json_request))
        assert response.status_code == 200
