import os
from dotenv import load_dotenv
from src.domain.entities.connection import Connection

from src.domain.entities.dashboard import Dashboard
from src.infrastructure.connections.social_factory import SocialFactory
from src.infrastructure.external_service.server_api import HttpService
from src.infrastructure.connections.base import BaseSocial
from src.application.dto.socials import TwitterDTO
import uuid

load_dotenv()


@SocialFactory.register("twitter")
class Twitter(BaseSocial):
    def __init__(
            self,
            *,
            connection: Connection,
            http_service: HttpService,
    ):
        self.http_service = http_service
        self.connection = connection

    async def get_statistic(self, *, post_url, company_id) -> Dashboard:
        twitter_dto = TwitterDTO(
            twitter_url=post_url,
            api_bright_token=os.environ["API_BRIGHT_DATA_TOKEN"],
            dataset_twitter=os.environ["DATASET_TWITTER"]
        )

        statistic = await self.http_service.send_request_twitter(twitter_dto)

        dashboard = Dashboard(
            id=uuid.uuid4(),
            social="twitter",
            company_id=company_id,
            statistic=statistic
        )
        return dashboard
