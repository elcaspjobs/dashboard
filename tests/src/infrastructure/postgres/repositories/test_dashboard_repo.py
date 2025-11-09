import pytest


@pytest.mark.asyncio
async def test_create_dashboard_repo(uow, dashboard_entity):
    dashboard_entity = await dashboard_entity()
    async with uow:
        result_entity = await uow.dashboard.create(dashboard_entity)

    assert result_entity == dashboard_entity


@pytest.mark.asyncio
async def test_get_dashboard_repo(uow, dashboard_entity):
    dashboard_entity = await dashboard_entity()
    async with uow:
        result_entity = await uow.dashboard.create(dashboard_entity)

    fetched = await uow.dashboard.get(dashboard_id=result_entity.id)
    assert fetched is not None
