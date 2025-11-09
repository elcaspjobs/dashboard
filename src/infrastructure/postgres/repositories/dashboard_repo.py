from sqlalchemy import insert, select
from src.infrastructure.postgres.repositories.base_repo import BaseRepository
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.engine import RowMapping
from src.infrastructure.postgres.tables import dashboard_table
from src.domain.entities.dashboard_entity import Dashboard
from uuid import UUID
from src.infrastructure.exceptions import ObjectDoesNotExistError


class DashboardRepository(BaseRepository):

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self, dashboard_data: Dashboard, **extra) -> Dashboard:
        await self.session.execute(
            insert(dashboard_table).values(
                id=dashboard_data.id,
                social=dashboard_data.social,
                company_id=dashboard_data.company_id,
                stats_kwargs=dashboard_data.stats_kwargs,
                created_at=dashboard_data.created_at,
            )
        )
        return dashboard_data

    async def get(self, *, dashboard_id: UUID) -> Dashboard:
        query = select(dashboard_table).where(dashboard_table.c.id == dashboard_id)
        result = await self.session.execute(query)
        row: RowMapping | None = result.mappings().first()
        if row is None:
            raise ObjectDoesNotExistError(
                repository="DashboardRepository",
                identifier=dashboard_id,
            )
        return Dashboard.from_orm(row)
