from src.domain.entities.connection import Connection
from src.domain.entities.dashboard import Dashboard
from src.infrastructure.connections.social_factory import SocialFactory
from src.infrastructure.external_service.server_api import HttpService
from src.infrastructure.connections.base import BaseSocial
from src.application.dto.socials import InstagramDTO

import uuid


@SocialFactory.register("instagram")
class Instagram(BaseSocial):
    def __init__(
            self,
            *,
            connection: Connection,
            http_service: HttpService,
    ):
        self.connection = connection
        self.http_service = http_service

    async def get_statistic(self, *, post_url, company_id) -> Dashboard:
        instagram_dto = InstagramDTO(
            post_id=post_url,
            access_token=self.connection.access_token,
            user_id=self.connection.account_id
        )
        statistic = await self.http_service.send_request_instagram(instagram_dto)
        return Dashboard(
            id=uuid.uuid4(),
            social="instagram",
            statistic=statistic,
            company_id=company_id
        )
