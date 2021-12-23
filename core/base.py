from abc import ABC, abstractmethod


class DatabaseObject(ABC):
    db_object = None

    @abstractmethod
    def save(self, *args, **kwargs):
        """Saves object to database"""
        pass

    def update(self, *args, **kwargs):
        """Updates object in database"""
        pass

    @classmethod
    @abstractmethod
    def load(cls, *args, **kwargs):
        """Loads object from database"""
        return cls()
