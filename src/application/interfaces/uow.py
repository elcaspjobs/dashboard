from abc import abstractmethod
from typing import Protocol


class UnitOfWork(Protocol):

    @abstractmethod
    async def commit(self):
        pass

    @abstractmethod
    async def rollback(self):
        pass


