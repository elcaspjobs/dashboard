import re

from src.domain.entities.connection import Connection
from src.domain.entities.dashboard import Dashboard
from src.infrastructure.connections.social_factory import SocialFactory
from src.infrastructure.external_service.server_api import HttpService
from src.infrastructure.connections.base import BaseSocial
from src.application.dto.socials import FacebookDTO
import uuid


@SocialFactory.register("facebook")
class Facebook(BaseSocial):
    def __init__(
            self,
            *,
            connection: Connection,
            http_service: HttpService,
    ):
        self.connection = connection
        self.http_service = http_service

    async def get_statistic(self, *, post_url, company_id) -> Dashboard:
        patterns = [
            r"/posts/(\d+)",  # /posts/123456
            r"story_fbid=(\d+)",  # permalink.php?story_fbid=123456&id=...
            r"/videos/(\d+)",  # /videos/123456
            r"fbid=(\d+)",  # photo.php?fbid=123456
        ]
        for pattern in patterns:
            match = re.search(pattern, post_url)
            if match:
                post_id = match.group(1)

                facebook_dto = FacebookDTO(
                    post_id=post_id,
                    access_token=self.connection.access_token,
                    user_id=self.connection.account_id
                )
                statistic = await self.http_service.send_request_facebook(facebook_dto)
                return Dashboard(
                    id=uuid.uuid4(),
                    social="facebook",
                    statistic=statistic,
                    company_id=company_id
                )
