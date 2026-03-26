from __future__ import annotations

import logging

from task import Task
from exceptions import TaskValidationError, TaskPriorityError, TaskDescriptionError
from system import GeneratorTaskSource, APIStubTaskSource, FileTaskSource, create_sample_file

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

def main() -> None:
    logger.info("Starting programm")
    