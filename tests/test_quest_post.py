from web.server.save_data import save_quest_data
from core.quest import Quest


def test_json_fixture(json_request):
    assert isinstance(json_request, dict)
    assert json_request["quest"]
    assert json_request["quest"] == "Важный вопрос"
    assert json_request["nodes"]
    assert len(json_request["nodes"]) == 3


def test_save_quest_data(session, json_request):
    Quest.set_session(session)
    # TODO Mock commit
    assert not save_quest_data(json_request, commit=False)
    quest = Quest.find(1)
    assert len(quest.get_nodes()) == 3
    assert quest.title == "Важный вопрос"
