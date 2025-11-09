import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine, AsyncEngine
from tests.conftest import config_setup
from src.infrastructure.postgres.tables import metadata
from src.infrastructure.postgres.uow import DashboardUnitOfWork


@pytest_asyncio.fixture
async def engine(config_setup) -> AsyncEngine:
    engine = create_async_engine(config_setup.db_dsn)
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
    yield DashboardUnitOfWork(session)
