from typing import Sequence

from sqlalchemy import insert, select
from src.infrastructure.postgres.repositories.base_repo import BaseRepository
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.engine import RowMapping
from src.infrastructure.postgres.tables import dashboard
from src.domain.entities.dashboard import Dashboard
from uuid import UUID
from src.infrastructure.exceptions import ObjectDoesNotExistError


class DashboardRepository(BaseRepository):

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self, dashboard_data: Dashboard) -> Dashboard:
        await self.session.execute(
            insert(dashboard).values(
                id=dashboard_data.id,
                social=dashboard_data.social,
                company_id=dashboard_data.company_id,
                statistic=dashboard_data.statistic,
            )
        )
        return dashboard_data

    async def bulk_create(
            self,
            dashboard_list: Sequence[Dashboard],
    ) -> Sequence[Dashboard]:
        if not dashboard_list:
            return []

        await self.session.execute(
            insert(dashboard).values(
                [
                    {
                        "id": task.id,
                        "social": task.social,
                        "company_id": task.company_id,
                        "statistic": task.statistic,
                    }
                    for task in dashboard_list
                ]
            )
        )

        return dashboard_list

    async def get(self, *, dashboard_id: UUID) -> Dashboard:
        query = select(dashboard).where(dashboard.c.id == dashboard_id)
        result = await self.session.execute(query)
        row: RowMapping | None = result.mappings().first()
        if row is None:
            raise ObjectDoesNotExistError(
                repository="DashboardRepository",
                identifier=dashboard_id,
            )
        return Dashboard.from_orm(row)
