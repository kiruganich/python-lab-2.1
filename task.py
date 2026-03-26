from __future__ import annotations
from dataclasses import dataclass
from typing import Protocol, Iterator, runtime_checkable, Any
from descriptors import ValidPayload, ValidPriority, ValidStatus
import uuid
import datetime


class Task:
    payload = ValidPayload()
    priority = ValidPriority()

    _status = ValidStatus()

    def __init__(self, payload : str = "None", priority : int = 10):
        self._id : str = str(uuid.uuid4())
        self._time : datetime = datetime.now()

        self.payload = payload
        self.priority = priority

        self.status: str = "new"

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

    @property
    def _set_status(self, status: str) -> None:
        self.status = status


    

    
    
    