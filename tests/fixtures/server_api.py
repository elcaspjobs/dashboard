import aiohttp
import pytest_asyncio
from src.infrastructure.external_service.server_api import HttpService


@pytest_asyncio.fixture
async def client_session(config):
    async with aiohttp.ClientSession(headers=config.server_header) as aio_session:
        yield aio_session


@pytest_asyncio.fixture
async def http_service(config, client_session, logger) -> HttpService:
    return HttpService(
        logger=logger,
        backend_url=config.server_api_url,
        http_session=client_session,
    )
