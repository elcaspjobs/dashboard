from abc import ABC, abstractmethod


class BaseRepository(ABC):

    @abstractmethod
    async def create(self, *args, **kwargs):
        pass

    @abstractmethod
    async def get(self, *args, **kwargs):
        pass


class GetRepository(ABC):
    @abstractmethod
    async def get(self, *args, **kwargs):
        pass
