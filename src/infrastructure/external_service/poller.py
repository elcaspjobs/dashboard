import ast
import asyncio
import json

import aiohttp
import structlog
from aiohttp import ClientSession

from src.infrastructure.exceptions import ErrorMessages, PollingError

MAX_RETRIES: int = 50 * 3
DEFAULT_DELAY: int = 3
TIMEOUT_RETRY_DELAY: int = 7
TIMEOUT_REQUEST: int = 10


class TaskPoller:
    def __init__(
        self,
        *,
        http_session: ClientSession,
        backend_url: str,
        logger: structlog.BoundLogger,
    ):
        self.http_session = http_session
        self.feed_backend_url = backend_url
        self.logger = logger

    async def poll_task(self, task_id: str) -> dict:
        self.logger.info(f"Запускаю метод poll_task для taskId={task_id}")

        url = self.feed_backend_url + "/task/checkTask"

        attempt = 0

        while attempt < MAX_RETRIES:
            attempt += 1

            try:

                async with self.http_session.get(
                    url,
                    params={"uuid": task_id},
                    timeout=aiohttp.ClientTimeout(total=TIMEOUT_REQUEST),
                ) as resp:

                    resp.raise_for_status()
                    response = await resp.json()

                    status = response.get("status")

                    match status:

                        case "done":
                            self.logger.info(
                                f"Задача {task_id} - выполнена\nКол-во попыток {attempt}"
                            )

                            raw_result = response["result"]["result"]

                            try:
                                parsed_result = json.loads(raw_result)
                            except json.JSONDecodeError:
                                self.logger.warning(
                                    "Некорректный JSON от сервера, пробую ast.literal_eval",
                                    raw_result=raw_result
                                )
                                try:
                                    parsed_result = ast.literal_eval(raw_result)
                                except Exception as e:
                                    raise ValueError(
                                        "Не удалось разобрать результат ни как JSON, "
                                        f"ни как Python literal: {raw_result}"
                                    ) from e

                            self.logger.info(
                                json.dumps(parsed_result, ensure_ascii=False, indent=2)
                            )

                            return parsed_result

                        case "failed":
                            self.logger.warning(f"Задача {task_id} - рухнула")

                            raise PollingError(f"{task_id} has failed")

                        case _:
                            self.logger.info(response)

            except (TimeoutError, aiohttp.ServerTimeoutError):
                self.logger.warning(
                    f"Таймаут при опросе задачи {task_id}. "
                    f"Попытка {attempt}/{MAX_RETRIES}, повтор через {TIMEOUT_RETRY_DELAY} сек."
                )
                await asyncio.sleep(TIMEOUT_RETRY_DELAY)
                continue

            except aiohttp.ClientError:
                self.logger.exception("Error during polling:")
                raise

            await asyncio.sleep(DEFAULT_DELAY)

        raise PollingError(
            ErrorMessages.RUNTIME_ERROR.format(
                f"poll_task finished without returning or raising properly\ntaskId={task_id}"
            )
        )
