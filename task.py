from __future__ import annotations
from dataclasses import dataclass
import uuid
from datetime import datetime

from descriptors import ValidPayload, ValidPriority, ValidStatus
from exceptions import TaskValidationError



class Task:

    """
    Модель задачи в платформе обработки задач.
    
    Атрибуты:
    1. Пользовательские (payload, priority) — валидация через дескрипторы
    2. Системные (id, status, created_at) — генерируются системой, read-only
    3. Вычисляемые (is_ready, is_active, age) — property

    """
        
    payload = ValidPayload()
    priority = ValidPriority()

    _status = ValidStatus()

    def __init__(self, payload : str = "None", priority : int = 10):

        # system attributes
        self._id : str = str(uuid.uuid4())
        self._time : datetime = datetime.now()

        # user attributes
        self.payload = payload
        self.priority = priority

        # initial state
        self._status: str = "new"

    # read-only methods

    @property
    def id(self) -> str:
        """Get ID"""
        return self._id
    
    @property
    def time(self) -> datetime:
        """Get initialization time"""
        return self._time
    
    @property
    def status(self) -> str:
        """Get task status"""
        return self._status
    
    # system methods

    def _set_status(self, status: str) -> None:
        """Set task status"""
        self._status = status

    def _mark_ready(self) -> None:
        """Change task status to "ready" """
        self._set_status("ready")

    def _mark_done(self) -> None:
        """Change task status to "done" """
        self._set_status("done")

    def _mark_processing(self) -> None:
        """Change task status to "processing" """
        self._set_status("processing")

    def _mark_cancelled(self) -> None:
        """Change task status to "cancelled" """
        self._set_status("cancelled")
    
    # computed properties

    @property
    def is_ready(self) -> bool:
        """Check if task is "ready" """
        return self._status == "ready"
    
    @property
    def is_active(self) -> bool:
        """Check if task is not "completed" or  "cancelled" yet"""
        return self.status not in {"completed", "cancelled"}
    
    @property
    def is_done(self) -> bool:
        """Check if task is "done" """
        return self._status == "done"
    
    @property
    def age(self) -> float:
        """Get the age of the task in seconds"""
        return (datetime.now() - self._time).total_seconds()
    
    #magic methods

    def __repr__(self) -> str:
        """Official string representation for debugging"""
        return (
            f"Task(id={self._id!r}, "
            f"payload={self.payload!r}, "
            f"priority={self.priority}, "
            f"status={self.status!r})"
        )
    
    def __eq__(self, other: object) -> bool:
        """Checking equality of tasks by identifier"""
        if not isinstance(other, Task):
            return NotImplemented
        return self._id == other._id
    
    