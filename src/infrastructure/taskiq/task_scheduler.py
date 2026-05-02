from src.application.interfaces.task_sheduler import TaskScheduler


class DashboardTaskScheduler(TaskScheduler):

    async def update_dashboard_data(self) -> str:
        from src.presentation.task_iq.tasks import schedule_task_dashboard

        task = await schedule_task_dashboard.defer()

        return task.task_id

