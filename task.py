from __future__ import annotations
from dataclasses import dataclass
from typing import Protocol, Iterator, runtime_checkable, Any
import uuid
from datetime import datetime

from descriptors import ValidPayload, ValidPriority, ValidStatus
from exceptions import TaskIDError, TaskPayloadError, TaskPriorityError, TaskStatusError



class Task:
    payload = ValidPayload()
    priority = ValidPriority()

    _status = ValidStatus()

    def __init__(self, payload : str = "None", priority : int = 10):
        self._id : str = str(uuid.uuid4())
        self._time : datetime = datetime.now()

        self.payload = payload
        self.priority = priority

        self._status: str = "new"

    #user methods

    @property
    def id(self) -> str:
        return self._id
    
    @property
    def time(self) -> datetime:
        return self._time
    
    @property
    def status(self) -> str:
        return self._status
    
    #system methods


    def _set_status(self, status: str) -> None:
        self._status = status

    def _mark_ready(self) -> None:
        self._set_status("ready")

    def _mark_done(self) -> None:
        self._set_status("done")

    def _mark_processing(self) -> None:
        self._set_status("processing")

    def _mark_cancelled(self) -> None:
        self._set_status("cancelled")
    

    @property
    def is_ready(self) -> bool:
        return self._status == "ready" and self.priority > 5
    
    @property
    def is_active(self) -> bool:
        return self.status not in {"completed", "cancelled"}
    
    @property
    def is_done(self) -> bool:
        return self._status == "done"
    
    @property
    def age(self) -> float:
        return (datetime.now() - self._time).total_seconds()
    
    #magic methods

    def __repr__(self) -> str:
        return (
            f"Task(id={self._id!r}, "
            f"description={self.description!r}, "
            f"priority={self.priority}, "
            f"status={self.status!r})"
        )
    
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Task):
            return NotImplemented
        return self._id == other._id
    
    