import pytest


@pytest.mark.asyncio
async def test_create_dashboard_repo(uow, dashboard_entity, logger):
    logger.info("TEST CREATE DASHBOARD REPO")

    result_entity = await uow.dashboard.create(dashboard_entity)
    await uow.commit()

    assert result_entity == dashboard_entity


@pytest.mark.asyncio
async def test_get_dashboard_repo(uow, dashboard_entity, logger):
    logger.info("TEST GET DASHBOARD REPO")

    result_entity = await uow.dashboard.create(dashboard_entity)
    await uow.commit()

    fetched = await uow.dashboard.get(dashboard_id=result_entity.id)
    assert fetched is not None
