from datetime import datetime, timezone, timedelta
from typing import Sequence

from src.infrastructure.postgres.repositories.base_repo import GetRepository
from src.domain.entities.connection import PublishResult
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from src.infrastructure.postgres.tables import connection_table, publication_table, feed_table
from src.domain.entities.connection import Connection


class PublicationsRepo(GetRepository):

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get(self, *, stmt) -> Sequence[PublishResult]:
        rows = await self.session.execute(stmt)
        result = rows.mappings().all()

        return [
            PublishResult(
                connection=Connection(
                    id=row.id,
                    social=row.social,
                    name=row.name,
                    account_id=row.account_id,
                    oauth_token=row.oauth_token,
                    access_token=row.access_token,
                    client_secret=row.client_secret,
                    refresh_token=row.refresh_token,
                    company_id=row.company_id
                ),
                result_url=row.result_url,
                company_id=row.company_id
            )
            for row in result
        ]

    async def filter_by_time(self) -> Sequence[PublishResult]:
        end_time = datetime.now(timezone.utc)
        start_time = end_time - timedelta(hours=6)

        social_list = ['twitter', 'linkedin', 'youtube', 'facebook', 'instagram']

        stmt = (
            select(
                connection_table,
                publication_table.c.result_url,
                feed_table.c.company_id
            )
            .select_from(publication_table)
            .join(feed_table, publication_table.c.feed_id == feed_table.c.id)
            .join(connection_table, publication_table.c.connection_id == connection_table.c.id)
            .where(
                publication_table.c.publish_time.between(start_time, end_time),
                func.lower(connection_table.c.social).in_(social_list)
            )
        )
        return await self.get(stmt=stmt)
