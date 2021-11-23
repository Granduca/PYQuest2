from tools import Container


class Quest:
    def __init__(self):
        self._title = ''
        self.nodes = Container(self)

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, title: str):
        self._title = title
