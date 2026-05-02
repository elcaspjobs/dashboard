import asyncio
import uuid
from uuid import UUID

import aiohttp
from aiohttp import ClientSession
import structlog
from src.domain.entities.dashboard import Dashboard
from src.infrastructure.exceptions import ErrorMessages
from src.infrastructure.external_service.poller import TaskPoller
from src.application.dto.socials import YoutubeDTO, LinkedinDTO, TwitterDTO, FacebookDTO, InstagramDTO


class HttpService:

    def __init__(
            self,
            *,
            http_session: ClientSession,
            backend_url: str,
            logger: structlog.BoundLogger
    ):
        self.http_session = http_session
        self.backend_url = backend_url
        self.logger = logger

        self.poller = TaskPoller(
            http_session=http_session,
            backend_url=backend_url,
            logger=logger,
        )

    async def send_request_youtube(self, data: YoutubeDTO) -> dict:

        meta_url = self.backend_url + "/metaconnect/youtube_statistics"
        return await self._send_request(url=meta_url, data=data, log_prefix="Youtube stats")

    async def send_request_linkedin(self, data: LinkedinDTO) -> dict:
        url = self.backend_url + "/metaconnect/linkedin_check_statistics"
        return await self._send_request(url=url, data=data, log_prefix="Linkedin ФИЗ stats")

    async def send_request_twitter(self, data: TwitterDTO) -> dict:
        url = self.backend_url + "/metaconnect/twitter_check_statistics"
        return await self._send_request(url=url, data=data, log_prefix="Twitter stats")

    async def send_request_facebook(self, data: FacebookDTO) -> dict:
        url = self.backend_url + "/metaconnect/facebook_check_statistics"
        return await self._send_request(url=url, data=data, log_prefix="Facebook stats")

    async def send_request_instagram(self, data: InstagramDTO) -> dict:
        url = self.backend_url + "/metaconnect/inst_check_statistics"
        return await self._send_request(url=url, data=data, log_prefix="Instagram stats")

    async def send_request_company_linkedin(self, data: LinkedinDTO) -> dict:
        url = self.backend_url + f"/metaconnect/linkedin_company_statistics"
        return await self._send_request(url=url, data=data, log_prefix="Linkedin company stats")

    async def _send_request(self, *, url: str, data, log_prefix: str) -> dict:
        response = await self.fetch_with_retries(url=url, json=data.to_dict())
        self.logger.info(f"{log_prefix}: запрос отправлен")

        statistics = await self.poller.poll_task(response["taskId"])
        self.logger.info(f"{log_prefix}: получена статистика {statistics}")

        return statistics

    async def fetch_with_retries(
            self, url: str, *, method="POST", json: dict, retries: int = 3, delay: int = 2
    ):
        attempt = 0
        while attempt < retries:
            attempt += 1

            async with self.http_session.request(
                    method, url, json=json, timeout=30,
            ) as resp:
                try:
                    resp.raise_for_status()
                    return await resp.json()
                except (TimeoutError, aiohttp.ClientError):
                    if attempt >= retries:
                        raise
                    await asyncio.sleep(delay)

        raise RuntimeError(
            ErrorMessages.RUNTIME_ERROR.format(
                "fetch_with_retries finished without returning or raising properly"))
