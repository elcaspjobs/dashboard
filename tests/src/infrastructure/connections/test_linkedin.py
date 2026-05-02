import pytest
from src.domain.entities.dashboard import Dashboard
from src.domain.entities.connection import Connection
from src.infrastructure.connections.linkedin import Linkedin
from faker import Faker
import os
faker = Faker()


@pytest.fixture
def connection_linkedin():
    return Connection(
        id=faker.random_int(1, 1000),
        social="linkedin",
        name=faker.word(),
        account_id=os.getenv("LINKEDIN_ACCOUNT_ID"),
        access_token=os.getenv("LINKEDIN_ACCESS_TOKEN"),
        linkedin_org=False
    )


@pytest.fixture
def connection_linkedin_company():
    return Connection(
        id=faker.random_int(1, 1000),
        social="linkedin",
        name=faker.word(),
        account_id=os.getenv("LINKEDIN_COMPANY_ID"),
        access_token=os.getenv("LINKEDIN_ACCESS_COMPANY_TOKEN"),
        linkedin_org=True
    )


@pytest.mark.skip
@pytest.mark.asyncio
async def test_connection_linkedin_classic(connection_linkedin, logger, http_service):
    logger.info("ЗАПУСК линкедин теста для физ лица")

    linkedin_fabric = Linkedin(
        connection=connection_linkedin,
        http_service=http_service
    )
    dashboard = await linkedin_fabric.get_statistic(
        post_url="https://www.linkedin.com/feed/update/urn:li:share:7398375062120308738")
    logger.info(f"dashboard linkedin: {dashboard}")
    assert dashboard is not None
    assert isinstance(dashboard, Dashboard)


@pytest.mark.skip
@pytest.mark.asyncio
async def test_connection_linkedin_company(connection_linkedin_company, logger, http_service):
    logger.info("ЗАПУСК линкедин теста для компании")

    linkedin_fabric = Linkedin(
        connection=connection_linkedin_company,
        http_service=http_service
    )
    dashboard = await linkedin_fabric.get_statistic(
        post_url="https://www.linkedin.com/feed/update/urn:li:share:7399447104622067712")

    logger.info(f"dashboard linkedin: {dashboard}")
    assert dashboard is not None
    assert isinstance(dashboard, Dashboard)
