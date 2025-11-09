from __future__ import annotations

from enum import Enum, auto
from uuid import UUID
import structlog


class ErrorMessages(Enum):
    OBJ_DOES_NOT_EXIST = "%s(id=%s) does not exist"
    CREATION_FAILED = "Failed to create %s with data: %s"
    DELETION_FAILED = "Failed to delete %s(id=%s)"
    INVALID_INPUT = "Invalid input for %s: %s"
    GENERIC_REPO_ERROR = "Repository error in %s: %s"
    NOT_IMPLEMENTED = "Not implemented method: %s"
    UNKNOWN_ERROR = "Unknown error: %s"
    COMMITTING_ERROR = "Committing error: %s"
    RUNTIME_ERROR = "Runtime error: %s"
    TASK_FAILED = "Task failed: %s"

    def format(self, *args):
        return self.value % args


class BaseError(Exception):
    def __init__(self, message: str, *, original_exception: Exception | None = None):
        self.message = message
        self.original_exception = original_exception

        logger = structlog.get_logger()
        logger.error(f"{self.__class__.__name__}: {self.message}")
        if original_exception:
            pass
        else:
            logger.exception(original_exception)

        super().__init__(message)


class BaseRepositoryError(BaseError):
    def __init__(self, message: str, *, original_exception: Exception | None = None):
        message = ErrorMessages.UNKNOWN_ERROR.format(message)
        super().__init__(message, original_exception=original_exception)


class CommittingError(BaseError):
    def __init__(self, message: str, *, original_exception: Exception | None = None):
        message = ErrorMessages.COMMITTING_ERROR.format(message)
        super().__init__(message, original_exception=original_exception)


class ObjectDoesNotExistError(BaseRepositoryError):
    def __init__(
        self,
        repository: str,
        identifier: str | int | UUID,
        *,
        original_exception: Exception | None = None,
    ):
        message = ErrorMessages.OBJ_DOES_NOT_EXIST.format(
            repository,
            identifier,
        )
        super().__init__(message=message, original_exception=original_exception)


class RecordDoesNotExistError(BaseRepositoryError):
    def __init__(
        self,
        repository: str,
        identifier: int | str,
        *,
        original_exception: Exception | None = None,
    ):
        message = ErrorMessages.OBJ_DOES_NOT_EXIST.format(repository, identifier)
        super().__init__(message, original_exception=original_exception)


class RecordCreationError(BaseRepositoryError):
    def __init__(
        self,
        obj_type: str,
        *,
        original_exception: Exception | None = None,
    ):
        message = ErrorMessages.CREATION_FAILED.format(obj_type)
        super().__init__(message, original_exception=original_exception)

