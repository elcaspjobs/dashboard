import datetime

import pytest_asyncio
from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine, AsyncEngine
from src.infrastructure.postgres.tables import metadata
from src.infrastructure.postgres.uow import UnitOfWorkImp
from faker import Faker
from src.infrastructure.postgres.tables import feed_table, connection_table, publication_table
import random

fake = Faker()

social = ["youtube", "instagram", "facebook", "twitter", "linkedin"]


@pytest_asyncio.fixture(scope="session")
async def engine(config) -> AsyncEngine:
    engine = create_async_engine(config.db_dsn)
    yield engine
    await engine.dispose()


@pytest_asyncio.fixture(scope="function", autouse=True)
async def setup_db(engine: AsyncEngine):
    async with engine.begin() as conn:
        await conn.run_sync(metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(metadata.drop_all)


@pytest_asyncio.fixture(scope="function")
async def session(engine):
    async_session = async_sessionmaker(
        engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )
    async with async_session() as session:
        yield session


@pytest_asyncio.fixture(scope="function")
async def uow(session):
    yield UnitOfWorkImp(session)


@pytest_asyncio.fixture
async def insert_feed(session):
    company_id = fake.random_int(1, 1000)
    result = await session.execute(insert(feed_table).values(
        company_id=company_id
    ).returning(feed_table)
                                   )
    row = result.fetchone()
    await session.commit()
    return row._mapping


@pytest_asyncio.fixture
async def insert_connection(session):
    async def _factory(**overrides):
        data = connection_factory(**overrides)

        result = await session.execute(
            insert(connection_table)
            .values(data)
            .returning(connection_table)
        )
        row = result.fetchone()
        await session.commit()
        return row._mapping

    return _factory


def connection_factory(**overrides):
    data = {
        "social": "youtube",
        "name": fake.name(),
        "token_status": True,
        "account_id": fake.uuid4(),
        "oauth_token": fake.sha1(),
        "access_token": fake.sha256(),
        "client_secret": fake.sha1(),
        "refresh_token": fake.sha256(),
        "linkedin_org": False,
    }

    # LinkedIn special flag
    if data["social"] == "linkedin":
        data["linkedin_org"] = True

    data.update(overrides)
    return data


@pytest_asyncio.fixture
def dirty_publication():
    def fabrick(publish_time: None):
        return {
            "publish_time": datetime.datetime.now() if not publish_time else publish_time,
            "result_url": fake.url()
        }

    return fabrick


@pytest_asyncio.fixture
async def publication_data(insert_feed, insert_connection, dirty_publication):
    async def _factory(**overrides):
        feed = insert_feed
        connection = await insert_connection()
        publish_time = overrides.get("publish_time")

        data = {
            "feed_id": feed["id"],
            "connection_id": connection["id"],
            **dirty_publication(publish_time=publish_time),
            **overrides,
        }

        return data

    return _factory


@pytest_asyncio.fixture
async def insert_publication(session, publication_data):
    async def _factory(**overrides):
        publication = await publication_data(**overrides)
        result = await session.execute(
            insert(publication_table).values(publication).returning(publication_table)
        )
        row = result.fetchone()
        await session.commit()
        return row._mapping

    return _factory
