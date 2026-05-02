from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Config:
    db_dsn: str
    rabbitmq: str
    server_api_url: str
    server_api_key: str
    test: bool

    @property
    def server_header(self):
        return {"X-API-Key": self.server_api_key}

