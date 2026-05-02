import pytest

from src.presentation.task_iq.tasks import schedule_task_dashboard


@pytest.mark.asyncio
async def test_tasks_dashboard(logger, dashboard_youtube_entity, mocker):
    youtube_entity = dashboard_youtube_entity
    logger.info("ЗАПУСК TASKIQ ТЕСТА")
    mocker.patch(
        "src.infrastructure.external_service.server_api.HttpService.send_request_youtube",
        return_value=youtube_entity,
    )

    task = await schedule_task_dashboard.kiq()
    task = await task.wait_result()
    logger.info("успешное выполнение таска")
    assert task.return_value is True
