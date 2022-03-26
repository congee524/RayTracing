from abc import ABC, abstractmethod


class Object(ABC):

    def __init__(self, name='object'):
        assert isinstance(name, str), "name of object must be str"
        self.name = name

    @abstractmethod
    def hit(self, ray, hit_record):
        pass
