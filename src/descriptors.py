from __future__ import annotations
import logging
from src.exceptions import TaskIDError, TaskPayloadError, TaskPriorityError, TaskStatusError
from typing import Any
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
            raise TaskPayloadError("Payload must be string")
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

    ALLOWED_TRANSITIONS: dict[str, frozenset[str]] = {
        "new": frozenset({"ready", "processing", "cancelled", "done"}),
        "ready": frozenset({"processing", "cancelled", "done"}),
        "processing": frozenset({"done", "cancelled", "ready"}),
        "done": frozenset(),
        "cancelled": frozenset(),
    }

    def __set_name__(self, owner, name) -> None:
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
        
        curr_status = getattr(instance, self.name, None)
        
        if curr_status is not None:
            if curr_status == normalized:
                return
            
            allowed_next = self.ALLOWED_TRANSITIONS.get(curr_status, frozenset())
            if normalized not in allowed_next:
                logger.error(f"Invalid transition: '{curr_status}' to '{normalized}'")
                raise TaskStatusError(f"Status transition not allowed: cannot change from {curr_status} to {normalized}")
        
        setattr(instance, self.name, normalized)
        logger.debug(f"Task status set to: {normalized}")


class ReadOnly:
    def __set_name__(self, owner, name) -> None:
        self.name = "_" + name

    def __get__(self, instance, owner) -> Any:
        if instance is None:
            return self
        return getattr(instance, self.name)
    
    def __set__(self, instance, value) -> None:
        if self.name in instance.__dict__:
            logger.error(f"Read-only violation: attempt to change '{self.name}'")
            raise AttributeError(f"'{self.name}' is read-only and cannot be modified after initialization")
        setattr(instance, self.name, value)
