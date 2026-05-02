import pytest
from src.infrastructure.config.config_storage import Config
from src.infrastructure.config.config_loader import load_forward_from_dotenv_file


@pytest.fixture(scope='session')
def config(logger) -> Config:
    config = load_forward_from_dotenv_file()
    logger.info(config)
    return config
