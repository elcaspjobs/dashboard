from dishka import Provider, provide, Scope
from src.application.interactors.dashboard_interactor import DashboardInteractor


class DashboardProvider(Provider):
    daily_dashboard_task = provide(
        DashboardInteractor,
        scope=Scope.REQUEST,
        provides=DashboardInteractor
    )
