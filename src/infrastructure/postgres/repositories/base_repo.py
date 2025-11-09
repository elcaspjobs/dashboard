from abc import ABC, abstractmethod


class BaseRepository(ABC):

    @abstractmethod
    def create(self, *args, **kwargs):
        pass

    @abstractmethod
    def get(self, *args, **kwargs):
        pass


