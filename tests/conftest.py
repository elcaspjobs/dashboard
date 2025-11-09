import pytest
import os
from src.core.logger import setup_logging
from src.infrastructure.config.config_storage import Config


@pytest.fixture(autouse=True)
def setup_test_logging():
    setup_logging()


@pytest.fixture(scope='function')
def config_setup():
    return Config(
        db_dsn=os.environ.get('DB_DSN'),
        rabbitmq=os.environ.get('RABBITMQ_URL'),
    )


pytest_plugins = [
    "tests.fixtures.database",
    "tests.fixtures.entities",
]


