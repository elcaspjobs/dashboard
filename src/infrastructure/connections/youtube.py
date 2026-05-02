import re
from src.domain.entities.connection import Connection
from src.domain.entities.dashboard import Dashboard
from src.infrastructure.external_service.server_api import HttpService
from src.infrastructure.connections.base import BaseSocial
from src.application.dto.socials import YoutubeDTO
from src.infrastructure.connections.social_factory import SocialFactory
import uuid


@SocialFactory.register("youtube")
class Youtube(BaseSocial):
    def __init__(self,
                 *,
                 connection: Connection,
                 http_service: HttpService,
                 ):
        self.connection = connection
        self.http_service = http_service

    async def get_statistic(self, *, post_url: str, company_id) -> Dashboard:
        pattern = r"(?:v=|youtu\.be/)([a-zA-Z0-9_-]{11})"

        match = re.search(pattern, post_url)
        post_id = match.group(1)

        youtube_dto = YoutubeDTO(
            access_token=self.connection.access_token,
            client_id=self.connection.account_id,
            client_secret=self.connection.client_secret,
            refresh_token=self.connection.refresh_token,
            video_id=post_id
        )

        statistics = await self.http_service.send_request_youtube(data=youtube_dto)

        return Dashboard(
            id=uuid.uuid4(),
            social="youtube",
            company_id=company_id,
            statistic=statistics
        )
