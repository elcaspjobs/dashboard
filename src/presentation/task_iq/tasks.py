import structlog
from dishka import FromDishka
from dishka.integrations.taskiq import inject
from src.presentation.task_iq.main import broker
from src.application.interactors.dashboard_interactor import DashboardInteractor


@broker.task(
    schedule=[{
        "cron": "0 */6 * * *"
    }
    ]
)
@inject(patch_module=True)
async def schedule_task_dashboard(
        interactor: FromDishka[DashboardInteractor],
        logger: FromDishka[structlog.BoundLogger]
):
    try:
        logger.info("Запуск обновления dashboard для youtube")
        await interactor()
        logger.info("Данные успешно загружены")
        return True
    except Exception as e:
        logger.error("Ошибка при обновлении dashboard статистики", error=str(e))
        logger.exception(e)


@broker.task(
    schedule=[
        {
            "cron": "0 */3 * * *"
        }
    ]
)
@inject(patch_module=True)
async def health_check(
        logger: FromDishka[structlog.BoundLogger],
):
    logger.info(f"Система в рабочем состоянии: SCHEDULER и WORKER РАБОТАЮТ")

    return True
