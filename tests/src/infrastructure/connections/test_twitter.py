import pytest
from src.domain.entities.dashboard import Dashboard
from src.infrastructure.connections.twitter import Twitter
from faker import Faker

faker = Faker()


@pytest.mark.skip
@pytest.mark.asyncio
async def test_twitter_connection(http_service, logger):
    logger.info("ТЕСТ ТВИТТЕРА СТАТИСТИКИ")
    twitter_fabric = Twitter(
        http_service=http_service,
    )
    result = await twitter_fabric.get_statistic(post_url="https://twitter.com/pur_saint/status/1992579097378107670")
    assert isinstance(result, Dashboard)
    logger.info(f"result twitter: {result.statistic}")


