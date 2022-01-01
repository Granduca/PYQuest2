from core import Quest


def test_quest(mem_session_maker):
    """Quest creation"""
    title = "Первый квест"
    Quest.session = mem_session_maker
    quest = Quest(title)
    quest.save()

    quest = Quest.load(quest.id)
    assert quest.title == title, "Название квеста не соответствует"
    assert not quest.get_networks(), "У нового квеста существуют сети нод"
