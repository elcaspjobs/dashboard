import os
import pytest
import faker

from src.domain.entities.dashboard import Dashboard
from src.domain.entities.connection import Connection

from src.infrastructure.connections.youtube import Youtube

faker = faker.Faker()


@pytest.fixture
def connection_youtube():
    return Connection(
        id=faker.random_int(1, 1000),
        social="youtube",
        name=faker.word(),
        account_id=os.getenv("YOUTUBE_ACCOUNT_ID"),
        access_token=os.getenv("YOUTUBE_ACCESS_TOKEN"),
        client_secret=os.getenv("YOUTUBE_CLIENT_SECRET"),
        refresh_token=os.getenv("YOUTUBE_REFRESH_TOKEN"),
    )


@pytest.mark.asyncio
@pytest.mark.skip
async def test_youtube(config, logger, connection_youtube, http_service):
    logger.info("ЗАПУСТИЛСЯ ТЕСТ ЮТУБА СТАТИСТИКИ ИНТ")

    youtube_fabric = Youtube(
        connection=connection_youtube,
        http_service=http_service,
    )

    dashboard = await youtube_fabric.get_statistic(post_url="https://www.youtube.com/watch?v=uhywSob6ZZc")
    logger.info(f"dashboard: {dashboard}")
    assert dashboard is not None
    assert isinstance(dashboard, Dashboard)
