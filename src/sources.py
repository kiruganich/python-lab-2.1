from __future__ import annotations
from typing import Iterator
from pathlib import Path
import json
import logging
from random import randint

from src.task import Task

logger = logging.getLogger(__name__)


class FileTaskSource:
    """Источник - JSON-файл."""
    
    def __init__(self, filepath: str | Path) -> None:
        self.filepath = Path(filepath)
    
    def get_tasks(self) -> Iterator[Task]:
        if not self.filepath.exists():
            logger.warning(f"File not found: {self.filepath}")
            return
        
        logger.info(f"Reading tasks from: {self.filepath}")
        with open(self.filepath, "r", encoding="utf-8") as f:
            for item in json.load(f):
                yield Task(
                    payload=item.get("payload"),
                    priority=item.get("priority")
                )

class GeneratorTaskSource:

    """Источник задач - программная генерация."""

    def __init__(self, count: int = 5, prefix: str = "gen") -> None:
        self.count = count
        self.prefix = prefix

    def get_tasks(self) -> Iterator[Task]:
        logger.info(f"Generating {self.count} tasks")
        for i in range(self.count):
            yield Task(
                payload=f"Task type: {self.prefix}, Task number: {i}",
                priority=randint(1, 10)
            )

class APITaskSource:

    """Заглушка внешнего API-источника."""

    DEFAULT_TASKS = [
        {"payload": "Low priority task", "priority": 8},
        {"payload": "Medium priority task", "priority": 5},
        {"payload": "High priority task", "priority": 3},
        {"payload": "The highest priority task", "priority": 1}
    ]

    def __init__(self, mock_tasks: list[dict] | None = None) -> None:
        self.mock_tasks = mock_tasks or self.DEFAULT_TASKS.copy()

    def get_tasks(self) -> Iterator[Task]:
        logger.info(f"Returning {len(self.mock_tasks)} tasks from API")
        for item in self.mock_tasks:
            yield Task(
                payload=item["payload"],
                priority=item["priority"]
            )