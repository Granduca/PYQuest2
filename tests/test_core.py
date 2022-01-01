from core import Quest


def test_quest(memory_session):
    title = "Первый квест"
    Quest.session = memory_session
    quest = Quest(title)
    quest.save()

    quest = Quest.load(quest.id)
    assert quest.title == title, "Название квеста не соответствует"
    assert not quest.get_networks(), "У нового квеста существуют сети нод"
