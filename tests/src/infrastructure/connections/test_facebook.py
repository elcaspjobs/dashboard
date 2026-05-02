import os
import pytest

from src.domain.entities.connection import Connection
from src.domain.entities.dashboard import Dashboard
from src.infrastructure.connections.facebook import Facebook
from faker import Faker

faker = Faker()


@pytest.fixture
def facebook_connection():
    return Connection(
        id=faker.random_int(1, 1000),
        social="facebook",
        name=faker.word(),
        account_id=os.getenv("FACEBOOK_ACCOUNT_ID"),
        access_token=os.getenv("FACEBOOK_ACCESS_TOKEN"),
        linkedin_org=False
    )


@pytest.mark.skip
@pytest.mark.asyncio
async def test_facebook_connection(http_service, logger, facebook_connection):
    logger.info("ТЕСТ ФЭЙСБУКА СТАТИСТИКИ")
    facebook_dto = Facebook(
        connection=facebook_connection,
        http_service=http_service,
    )
    result = await facebook_dto.get_statistic(
        post_url="https://www.facebook.com/photo/?fbid=654338554365839&set=a.127485843717782")
    assert result is not None
    assert isinstance(result, Dashboard)
    logger.info(f"result facebook: {result.statistic}")
