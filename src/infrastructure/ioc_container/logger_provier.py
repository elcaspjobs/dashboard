import sys
import logging
import structlog
from dishka import Provider, Scope, provide
from structlog.processors import TimeStamper, add_log_level, StackInfoRenderer, CallsiteParameterAdder, CallsiteParameter
from structlog.stdlib import LoggerFactory, BoundLogger


class LoggerProvider(Provider):
    @provide(scope=Scope.APP)
    async def get_logger(
            self,
    ) -> structlog.BoundLogger:
        console_handler = logging.StreamHandler(sys.stdout)
        console_formatter = logging.Formatter("%(message)s")
        console_handler.setFormatter(console_formatter)

        root_logger = logging.getLogger()
        root_logger.handlers.clear()
        root_logger.addHandler(console_handler)
        root_logger.setLevel(logging.INFO)

        structlog.configure(
            processors=[
                add_log_level,
                StackInfoRenderer(),
                TimeStamper(fmt="iso"),
                CallsiteParameterAdder(
                    [
                        CallsiteParameter.FILENAME,
                        CallsiteParameter.LINENO,
                        CallsiteParameter.FUNC_NAME,
                        CallsiteParameter.MODULE,
                        CallsiteParameter.PATHNAME,
                    ]
                ),
                structlog.dev.ConsoleRenderer(colors=True),
            ],
            context_class=dict,
            logger_factory=LoggerFactory(),
            wrapper_class=BoundLogger,
            cache_logger_on_first_use=True,
        )

        return structlog.get_logger()
