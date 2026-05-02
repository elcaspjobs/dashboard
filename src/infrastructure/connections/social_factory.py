from .base import BaseSocial
from src.domain.entities.connection import Connection
from src.infrastructure.external_service.server_api import HttpService


class SocialFactory:
    _registry: dict[str, type[BaseSocial]] = {}

    @classmethod
    def register(cls, name: str):
        """Декоратор для регистрации класса соцсети."""

        def decorator(social_cls: type[BaseSocial]):
            cls._registry[name] = social_cls
            return social_cls

        return decorator

    @classmethod
    def create(cls, *, social: str, connection: Connection, http_service: HttpService) -> BaseSocial | None:
        try:
            social_cls = cls._registry[social.lower()]
            return social_cls(connection=connection, http_service=http_service)

        except KeyError:
            return None
