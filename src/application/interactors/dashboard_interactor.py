import asyncio
from typing import Sequence

import structlog
from src.infrastructure.postgres.uow import UnitOfWorkImp
from src.infrastructure.external_service.server_api import HttpService
from src.domain.entities.dashboard import Dashboard
from src.infrastructure.connections.social_factory import SocialFactory
from dataclasses import is_dataclass


class DashboardInteractor:
    def __init__(
            self,
            logger: structlog.BoundLogger,
            uow: UnitOfWorkImp,
            http_service: HttpService,
    ):
        self.logger = logger
        self.uow = uow
        self.http_service = http_service

    async def __call__(self) -> None:
        publications = await self.uow.publication.filter_by_time()
        self.logger.info("Публикациии за выбранное время")
        self.logger.info([publish.connection.social for publish in publications])
        tasks = []

        for publish in publications:
            social = SocialFactory.create(
                connection=publish.connection,
                http_service=self.http_service,
                social=publish.connection.social
            )
            if social is None:
                self.logger.info(f"Неизвестная соц сеть {publish.connection.social}")
                continue

            self.logger.info(f"Получаем статистику {publish.connection.social}")

            tasks.append(social.get_statistic(post_url=publish.result_url, company_id=publish.company_id))

        dashboard_statistic: Sequence[Dashboard] = await asyncio.gather(*tasks, return_exceptions=True)
        dashboard_statistic = [dashboard for dashboard in dashboard_statistic if is_dataclass(dashboard)]
        self.logger.info("добавляем статистику в дашборд")

        await self.uow.dashboard.bulk_create(dashboard_list=dashboard_statistic)

        await self.uow.commit()
