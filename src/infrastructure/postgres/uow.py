from sqlalchemy.exc import SQLAlchemyError

from src.infrastructure.exceptions import CommittingError
from src.application.interfaces.uow import UnitOfWork
from sqlalchemy.ext.asyncio import AsyncSession
from src.infrastructure.postgres.repositories.dashboard_repo import DashboardRepository
from src.infrastructure.postgres.repositories.publications_repo import PublicationsRepo


class UnitOfWorkImp(UnitOfWork):

    def __init__(self, session: AsyncSession):
        self.session = session
        self.dashboard = DashboardRepository(session)
        self.publication = PublicationsRepo(session)

    async def commit(self) -> None:
        try:
            await self.session.commit()
        except SQLAlchemyError as e:
            await self.rollback()
            raise CommittingError(str(e)) from e

    async def rollback(self) -> None:
        await self.session.rollback()
