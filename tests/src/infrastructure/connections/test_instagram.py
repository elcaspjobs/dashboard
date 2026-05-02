import os
import pytest

from src.domain.entities.connection import Connection
from src.domain.entities.dashboard import Dashboard
from src.infrastructure.connections.instagram import Instagram
from faker import Faker

faker = Faker()


@pytest.fixture
def instagram_connection():
    return Connection(
        id=faker.random_int(1, 1000),
        social="instagram",
        name=faker.word(),
        account_id=os.getenv("INSTAGRAM_ACCOUNT_ID"),
        access_token=os.getenv("INSTAGRAM_ACCESS_TOKEN"),
        linkedin_org=False
    )


@pytest.mark.skip
@pytest.mark.asyncio
async def test_instagram_connection(http_service, logger, instagram_connection):
    logger.info("ТЕСТ ИНСТАГРАМ СТАТИСТИКИ")
    instagram_dto = Instagram(
        connection=instagram_connection,
        http_service=http_service,
    )
    result = await instagram_dto.get_statistic(post_url="https://www.instagram.com/reel/DRKXSxCj_6o/")
    assert result is not None
    assert isinstance(result, Dashboard)
    logger.info(f"result facebook: {result.statistic}")
