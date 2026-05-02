from dishka import make_async_container
from dishka.integrations.taskiq import setup_dishka
from taskiq_aio_pika import AioPikaBroker
from taskiq import InMemoryBroker, TaskiqEvents, TaskiqState
from taskiq import TaskiqScheduler
from taskiq.schedule_sources import LabelScheduleSource

from src.infrastructure.config.config_loader import load_forward_from_dotenv_file
from src.infrastructure.config.config_storage import Config
from src.infrastructure.ioc_container import (
    LoggerProvider,
    HttpProvider,
    DashboardProvider,
    SessionProvider,
)

config = load_forward_from_dotenv_file()
broker = InMemoryBroker(await_inplace=True) if config.test else AioPikaBroker(config.rabbitmq)

scheduler = TaskiqScheduler(
    broker=broker,
    sources=[LabelScheduleSource(broker)],
)
container = make_async_container(
    LoggerProvider(),
    HttpProvider(),
    DashboardProvider(),
    SessionProvider(),
    context={Config: config}
)

setup_dishka(container, broker=broker)
