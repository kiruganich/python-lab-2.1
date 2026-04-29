from __future__ import annotations
from typing import Iterator, runtime_checkable, Protocol, Any
from pathlib import Path
import json
import logging

from src.task import Task
from src.exceptions import TaskSourceValidationError

logger = logging.getLogger(__name__)

@runtime_checkable
class TaskSource(Protocol):
    """
    Контракт для источников задач

    """
    def get_tasks(self) -> Iterator[Task]:
        ...



def create_sample_file(filepath: str | Path, tasks: list[dict]) -> Path:

    """Create test JSON-file"""
    
    path = Path(filepath)
    logger.debug(f"Creating sample file: {path} with {len(tasks)} tasks")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(tasks, f, indent=2, ensure_ascii=False)
    logger.info(f"Sample file created: {path}")
    return path

def validate_source(source: Any) -> None:
    """
    Проверить объект на соответствие протоколу TaskSource

    """
    if not isinstance(source, TaskSource):
        logger.error(f"Expected TaskSource, got {type(source).__name__}")
        raise TaskSourceValidationError(f"TaskSource validation failed: Expected TaskSource, got {type(source).__name__}")
    logger.debug(f"Task source is valid")