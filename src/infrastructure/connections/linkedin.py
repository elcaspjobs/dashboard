import re

from src.domain.entities.connection import Connection
from src.domain.entities.dashboard import Dashboard
from src.infrastructure.connections.base import BaseSocial
from src.infrastructure.external_service.server_api import HttpService
from src.application.dto.socials import LinkedinDTO
from src.infrastructure.connections.social_factory import SocialFactory
import uuid

@SocialFactory.register("linkedin")
class Linkedin(BaseSocial):

    def __init__(self,
                 *,
                 connection: Connection,
                 http_service: HttpService,
                 ):
        self.connection = connection
        self.http_service = http_service

    async def get_statistic(self, *, post_url: str, company_id) -> Dashboard:
        match = re.search(r"(urn:li:share:\d+)", post_url)
        post_id = match.group(1) if match else None
        linkedin_org = self.connection.linkedin_org
        linkedin_dto = LinkedinDTO(
            post_id=post_id,
            token=self.connection.access_token,
            account_id=f"urn:li:organization:{self.connection.account_id}" if linkedin_org else None,
        )
        if linkedin_org:
            statistic = await self.http_service.send_request_company_linkedin(data=linkedin_dto)
        else:
            statistic = await self.http_service.send_request_linkedin(data=linkedin_dto)

        return Dashboard(
            id=uuid.uuid4(),
            social="linkedin",
            statistic=statistic,
            company_id=company_id,
        )
