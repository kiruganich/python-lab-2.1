from __future__ import annotations
import logging
from exceptions import TaskIDError, TaskPayloadError, TaskPriorityError, TaskStatusError
logger = logging.getLogger(__name__)

class ValidPayload:
    def __set_name__(self, owner, name) -> None:
        self.name = "_" + name

    def __get__(self, instance, owner) -> str:
        if instance is None:
            return self
        return getattr(instance, self.name)
    
    def __set__(self, instance, value) -> None:
        if not isinstance(value, str):
            logger.error("Payload validation failed: Payload must be string")
            raise TaskPayloadError("Paylod must be string")
        setattr(instance, self.name, value)


class ValidPriority:
    MIN_VALUE = 1
    MAX_VALUE = 10

    def __set_name__(self, owner, name) -> None: 
        self.name = "_" + name

    def __get__(self, instance, owner) -> int:
        if instance is None:
            return self
        return getattr(instance, self.name)
    
    def __set__(self, instance, value) -> None:
        if not isinstance(value, int) or isinstance(value, bool):
            logger.error("Priority validation failed: Priority must be integer")
            raise TaskPriorityError("Priority must be integer")
        if not self.MIN_VALUE <= value <= self.MAX_VALUE:
            logger.error("Priority validation failed: Priority must be from 1 to 10")
            raise TaskPriorityError("Priority must be from 1 to 10")
        setattr(instance, self.name, value)
        


class ValidStatus:
    VALID_STATUSES = frozenset({
        "new",
        "ready",
        "processing",
        "done",
        "cancelled"
    })

    def __set_name__(self, owmer, name) -> None:
        self.name = "_" + name

    def __get__(self, instance, owner) -> str:
        if instance is None:
            return self
        return getattr(instance, self.name)
    
    def __set__(self, instance, value) -> None:
        if not isinstance(value, str):
            logger.error("Status must be string")
            raise TaskStatusError("Status validation failed: Status must be string")
        normalized = value.lower().strip()

        if normalized not in self.VALID_STATUSES:
            logger.error("Invalid status")
            raise TaskStatusError("Status validation failed: Invalid status")
        setattr(instance, self.name, normalized)



