class Quest:
    def __init__(self):
        self._title = ''

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, title: str):
        self._title = title
