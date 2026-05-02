from abc import abstractmethod
from typing import Protocol


class TaskScheduler(Protocol):

    @abstractmethod
    async def update_dashboard_data(self) -> str: ...
