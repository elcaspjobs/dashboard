from aiohttp import ClientSession
from collections.abc import AsyncGenerator
from dishka import Provider, provide, Scope, from_context
from typing import Any
import structlog
from src.infrastructure.config.config_storage import Config
from src.infrastructure.external_service.server_api import HttpService


class HttpProvider(Provider):
    context = from_context(Config, scope=Scope.APP)

    @provide(scope=Scope.REQUEST)
    async def get_http_session(self, config: Config) -> AsyncGenerator[ClientSession, Any]:
        async with ClientSession(headers=config.server_header) as session:
            yield session

    @provide(scope=Scope.REQUEST)
    async def get_stat_service(
            self, http_session: ClientSession, config: Config, logger: structlog.BoundLogger
    ) -> HttpService:
        return HttpService(http_session=http_session, backend_url=config.server_api_url, logger=logger)
