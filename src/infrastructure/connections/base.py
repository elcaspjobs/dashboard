from abc import ABC, abstractmethod


class BaseSocial(ABC):

    @abstractmethod
    async def get_statistic(self, *args, **kwargs): ...
