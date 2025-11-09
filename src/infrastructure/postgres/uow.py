from sqlalchemy.exc import SQLAlchemyError

from src.infrastructure.exceptions import CommittingError
from src.application.interfaces.uow import UnitOfWork
from sqlalchemy.ext.asyncio import AsyncSession
from src.infrastructure.postgres.repositories.dashboard_repo import DashboardRepository


class DashboardUnitOfWork(UnitOfWork):

    def __init__(self, session: AsyncSession):
        self.session = session
        self.dashboard = DashboardRepository(session)

    async def commit(self):
        try:
            await self.session.commit()
        except SQLAlchemyError as e:
            await self.rollback()
            raise CommittingError(str(e)) from e

    async def rollback(self) -> None:
        await self.session.rollback()

    async def __aenter__(self):
        self.transaction = self.session.begin()
        await self.transaction.__aenter__()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.transaction.__aexit__(exc_type, exc_val, exc_tb)
