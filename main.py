from __future__ import annotations
from pathlib import Path

import logging

from task import Task
from exceptions import TaskValidationError, TaskPriorityError, TaskPayloadError
from system import GeneratorTaskSource, APITaskSource, FileTaskSource, create_sample_file

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

def demo_task() -> None:

    """Task model demonstration: descriptors and property."""

    logger.info("\nTask class demonstration")
    task = Task(
        payload="Demo user task",
        priority=8
    )
    logger.info(f"Task created: id={task.id}")
    logger.info(f"Payload: {task.payload}")
    logger.info(f"Priority: {task.priority}")
    logger.info(f"Status: {task.status}")
    logger.info(f"Created at: {task.time}")

    logger.info("Safety check: trying to change task ID")
    try:
        task.id = "hacked"
    except AttributeError as e:
        print(f"Access denied: {e}")

    task.payload = "Updated payload"
    task.priority = 3
    logger.info(f"payload was updated: {task.payload}")
    logger.info(f"priority was updated: {task.priority}")

    logger.info("Safety check: trying to set invalid priority")
    try:
        task.priority = 666
    except TaskPriorityError as e:
        print(f"Priority validation: {e}")

    logger.info("Safety check: trying to set invalid payload")
    try:
        task.payload = [1, 2, 3]
    except TaskPayloadError as e:
        print(f"Payload validation: {e}")
    
    task._set_status("ready")

    logger.info(f"is_ready = {task.is_ready} (status='{task.status}', priority={task.priority})")
    logger.info(f"is_active = {task.is_active}")
    logger.info(f"age = {task.age} sec")


def demo_sources() -> None:
    """Task sources demonstration."""

    logger.info("\nReturning task from sources demonstration")
    # Source: Generator
    gen_source = GeneratorTaskSource(count=2, prefix="gen")
    for i, task in enumerate(gen_source.get_tasks(), 1):
        logger.info(f"{i}. {task}")
    
    # Source: API
    logger.info("\nAPITaskSource:")
    api_source = APITaskSource()
    for i, task in enumerate(api_source.get_tasks(), 1):
        logger.info(f"      {i}. {task}")
    
    # Source: File
    logger.info("\nFileTaskSource:")
    test_file = Path("demo_tasks_lab2.json")
    sample_data = [
        {"payload": "File task #1", "priority": 7},
        {"payload": "File task #2", "priority": 2},
    ]
    create_sample_file(test_file, sample_data)
    
    file_source = FileTaskSource(test_file)
    for i, task in enumerate(file_source.get_tasks(), 1):
        logger.info(f"      {i}. {task}")
    
    test_file.unlink()
    logger.info("\nSample file deleted")

def main() -> None:

    try:
        logger.info("Demonstration started.")

        demo_task()

        demo_sources()

        logger.info("Demonstration completed.")
    
    except TaskValidationError as e:
        logger.error(f"Validation error: {e}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise

if __name__ == "__main__":
    main()