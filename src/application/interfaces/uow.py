from abc import abstractmethod
from typing import Protocol


class UnitOfWork(Protocol):

    @abstractmethod
    def commit(self):
        pass

    @abstractmethod
    def rollback(self):
        pass
