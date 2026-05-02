import os

from dotenv import load_dotenv

from src.infrastructure.config.config_storage import Config


def load_config_from_env() -> Config:
    return Config(
        db_dsn=os.environ["DB_DSN"],
        rabbitmq=os.environ["RABBITMQ_URL"],
        server_api_url=os.environ["SERVER_API"],
        server_api_key=os.environ["SERVER_API_KEY"],
        test=os.environ.get("TEST") == "true",
    )


def load_forward_from_dotenv_file() -> Config:
    load_dotenv()
    return load_config_from_env()


