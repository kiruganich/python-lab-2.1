from __future__ import annotations

import time
import pytest
from datetime import datetime, timedelta
from unittest.mock import patch, MagicMock

from task import Task
from descriptors import ValidPayload, ValidPriority, ValidStatus
from exceptions import (
    TaskValidationError,
    TaskPayloadError,
    TaskPriorityError,
    TaskStatusError,
)


class TestValidPayload:
    """Tests for task payload validation descriptor."""

    def test_valid_string_accepted(self):
        task = Task(payload="Test task", priority=5)
        assert task.payload == "Test task"

    def test_empty_string_accepted(self):
        task = Task(payload="", priority=5)
        assert task.payload == ""

    def test_non_string_rejected(self):
        with pytest.raises(TaskPayloadError, match="Payload must be string"):
            Task(payload=123, priority=5)  # type: ignore

    def test_list_rejected(self):
        task = Task(payload="Initial", priority=5)
        with pytest.raises(TaskPayloadError):
            task.payload = [1, 2, 3]  # type: ignore

    def test_none_rejected(self):
        with pytest.raises(TaskPayloadError):
            Task(payload=None, priority=5)  # type: ignore

    def test_payload_update_valid(self):
        task = Task(payload="Old", priority=5)
        task.payload = "New value"
        assert task.payload == "New value"


class TestValidPriority:
    """Tests for task priority validation descriptor."""

    @pytest.mark.parametrize("value", [1, 5, 10])
    def test_valid_priority_range(self, value: int):
        task = Task(payload="Test", priority=value)
        assert task.priority == value

    @pytest.mark.parametrize("value", [0, 11, -1, 100])
    def test_priority_out_of_range(self, value: int):
        with pytest.raises(TaskPriorityError, match="from 1 to 10"):
            Task(payload="Test", priority=value)

    def test_priority_not_integer(self):
        with pytest.raises(TaskPriorityError, match="must be integer"):
            Task(payload="Test", priority=5.5)  # type: ignore

    def test_bool_rejected_as_priority(self):
        with pytest.raises(TaskPriorityError):
            Task(payload="Test", priority=True)  # type: ignore

    def test_priority_string_rejected(self):
        with pytest.raises(TaskPriorityError):
            Task(payload="Test", priority="5")  # type: ignore

    def test_priority_update_valid(self):
        task = Task(payload="Test", priority=5)
        task.priority = 3
        assert task.priority == 3

    def test_priority_update_invalid(self):
        task = Task(payload="Test", priority=5)
        with pytest.raises(TaskPriorityError):
            task.priority = 15
        assert task.priority == 5


class TestValidStatus:
    """Tests for task status validation descriptor."""

    @pytest.mark.parametrize("status", ["new", "ready", "processing", "done", "cancelled"])
    def test_valid_statuses(self, status: str):
        task = Task(payload="Test", priority=5)
        task._set_status(status)
        assert task.status == status

    def test_status_case_insensitive(self):
        task = Task(payload="Test", priority=5)
        task._set_status("READY")
        assert task.status == "ready"

    def test_status_stripped(self):
        task = Task(payload="Test", priority=5)
        task._set_status("  done  ")
        assert task.status == "done"

    @pytest.mark.parametrize("invalid", ["unknown", "pending", "archived", ""])
    def test_invalid_status_rejected(self, invalid: str):
        task = Task(payload="Test", priority=5)
        with pytest.raises(TaskStatusError, match="Invalid status"):
            task._set_status(invalid)

    def test_status_non_string_rejected(self):
        task = Task(payload="Test", priority=5)
        with pytest.raises(TaskStatusError, match="must be string"):
            task._set_status(123)  # type: ignore


class TestTaskInitialization:
    """Tests for Task creation and system-generated attributes."""

    def test_default_values(self):
        task = Task()
        assert task.payload == "None"
        assert task.priority == 10
        assert task.status == "new"

    def test_custom_initialization(self):
        task = Task(payload="Custom task", priority=7)
        assert task.payload == "Custom task"
        assert task.priority == 7
        assert task.status == "new"

    def test_id_is_uuid_string(self):
        task = Task(payload="Test", priority=5)
        assert isinstance(task.id, str)
        assert len(task.id) == 36

    def test_id_is_readonly(self):
        task = Task(payload="Test", priority=5)
        original_id = task.id
        with pytest.raises(AttributeError):
            task.id = "hacked"  # type: ignore
        assert task.id == original_id

    def test_time_is_datetime(self):
        task = Task(payload="Test", priority=5)
        assert isinstance(task.time, datetime)

    def test_time_is_readonly(self):
        task = Task(payload="Test", priority=5)
        original_time = task.time
        with pytest.raises(AttributeError):
            task.time = datetime.now()  # type: ignore
        assert task.time == original_time

    def test_status_readonly_public(self):
        task = Task(payload="Test", priority=5)
        assert task.status == "new"


class TestTaskProperties:
    """Tests for computed task properties."""

    def test_is_ready_false_by_default(self):
        task = Task(payload="Test", priority=5)
        assert task.is_ready is False

    def test_is_ready_true_when_set(self):
        task = Task(payload="Test", priority=5)
        task._set_status("ready")
        assert task.is_ready is True

    def test_is_active_for_new_status(self):
        task = Task(payload="Test", priority=5)
        assert task.is_active is True

    def test_is_active_for_processing(self):
        task = Task(payload="Test", priority=5)
        task._set_status("processing")
        assert task.is_active is True

    def test_is_active_false_when_cancelled(self):
        task = Task(payload="Test", priority=5)
        task._set_status("cancelled")
        assert task.is_active is False

    def test_is_done(self):
        task = Task(payload="Test", priority=5)
        assert task.is_done is False
        task._set_status("done")
        assert task.is_done is True

    def test_age_positive(self):
        task = Task(payload="Test", priority=5)
        assert task.age >= 0

    def test_age_increases_over_time(self):
        task = Task(payload="Test", priority=5)
        age1 = task.age
        time.sleep(0.1)
        age2 = task.age
        assert age2 > age1

    @patch("task.datetime")
    def test_age_with_mocked_time(self, mock_datetime):
        fixed_time = datetime(2024, 1, 1, 12, 0, 0)
        later_time = datetime(2024, 1, 1, 12, 0, 30)
        
        mock_datetime.now.side_effect = [fixed_time, later_time]
        mock_datetime.side_effect = lambda *args, **kw: datetime(*args, **kw)
        
        task = Task(payload="Test", priority=5)
        assert task.age == 30.0


class TestTaskStatusMethods:
    """Tests for task status management methods."""

    def test_mark_ready(self):
        task = Task(payload="Test", priority=5)
        task._mark_ready()
        assert task.status == "ready"
        assert task.is_ready is True

    def test_mark_done(self):
        task = Task(payload="Test", priority=5)
        task._mark_done()
        assert task.status == "done"
        assert task.is_done is True

    def test_mark_processing(self):
        task = Task(payload="Test", priority=5)
        task._mark_processing()
        assert task.status == "processing"

    def test_mark_cancelled(self):
        task = Task(payload="Test", priority=5)
        task._mark_cancelled()
        assert task.status == "cancelled"
        assert task.is_active is False

    def test_set_status_via_descriptor(self):
        task = Task(payload="Test", priority=5)
        task._set_status("ready")
        assert task.status == "ready"
        
        with pytest.raises(TaskStatusError):
            task._set_status("invalid_status")


class TestTaskMagicMethods:
    """Tests for Task special methods."""

    def test_repr_contains_key_fields(self):
        task = Task(payload="Important task", priority=9)
        repr_str = repr(task)
        
        assert "Task(" in repr_str
        assert "payload='Important task'" in repr_str
        assert "priority=9" in repr_str
        assert "status='new'" in repr_str
        assert "id=" in repr_str

    def test_eq_same_id(self):
        task1 = Task(payload="Test", priority=5)
        task2 = Task(payload="Other", priority=1)
        task2._id = task1.id  # type: ignore
        
        assert task1 == task2

    def test_eq_different_id(self):
        task1 = Task(payload="Test 1", priority=5)
        task2 = Task(payload="Test 2", priority=5)
        assert task1 != task2

    def test_eq_with_non_task(self):
        task = Task(payload="Test", priority=5)
        result = task.__eq__("not a task")
        assert result is NotImplemented
        assert task != "not a task"

    def test_eq_not_implemented_handled(self):
        task = Task(payload="Test", priority=5)
        assert (task == None) is False  # type: ignore


class TestTaskWorkflow:
    """Integration tests for task lifecycle."""

    def test_full_task_lifecycle(self):
        task = Task(payload="Buy groceries", priority=7)
        assert task.status == "new"
        assert task.is_active is True
        
        task.payload = "Buy groceries and milk"
        task.priority = 3
        assert task.payload == "Buy groceries and milk"
        assert task.priority == 3
        
        task._mark_processing()
        assert task.status == "processing"
        assert task.is_active is True
        assert task.is_ready is False
        
        task._mark_done()
        assert task.status == "done"
        assert task.is_active is True
        assert task.is_done is True

    def test_validation_prevents_invalid_state(self):
        task = Task(payload="Test", priority=5)
        
        with pytest.raises(TaskPriorityError):
            task.priority = 100
        assert task.priority == 5
        
        with pytest.raises(TaskStatusError):
            task._set_status("archived")
        assert task.status == "new"

    def test_exception_hierarchy(self):
        assert issubclass(TaskPayloadError, TaskValidationError)
        assert issubclass(TaskPriorityError, TaskValidationError)
        assert issubclass(TaskStatusError, TaskValidationError)
        
        task = Task(payload="Test", priority=5)
        caught = False
        try:
            task.priority = "invalid"  # type: ignore
        except TaskValidationError:
            caught = True
        assert caught is True


class TestTaskEdgeCases:
    """Tests for edge cases and protection against misuse."""

    def test_descriptor_access_on_class(self):
        assert isinstance(Task.payload, ValidPayload)
        assert isinstance(Task.priority, ValidPriority)
        assert isinstance(Task._status, ValidStatus)

    def test_payload_with_special_characters(self):
        task = Task(payload="Task with emoji 🚀 and special: !@#$%", priority=5)
        assert task.payload == "Task with emoji 🚀 and special: !@#$%"

    def test_very_long_payload(self):
        long_text = "A" * 10000
        task = Task(payload=long_text, priority=5)
        assert task.payload == long_text
        assert len(task.payload) == 10000

    def test_priority_boundary_values(self):
        task_min = Task(payload="Min", priority=1)
        task_max = Task(payload="Max", priority=10)
        assert task_min.priority == 1
        assert task_max.priority == 10

    def test_multiple_tasks_independence(self):
        task1 = Task(payload="First", priority=5)
        task2 = Task(payload="Second", priority=8)
        
        task1.priority = 1
        task2.priority = 10
        
        assert task1.priority == 1
        assert task2.priority == 10
        assert task1.payload == "First"
        assert task2.payload == "Second"


@pytest.mark.parametrize("payload,priority,expected_status", [
    ("Simple task", 5, "new"),
    ("", 1, "new"),
    ("Urgent!", 10, "new"),
    ("Low priority", 1, "new"),
])
def test_task_creation_variations(payload: str, priority: int, expected_status: str):
    task = Task(payload=payload, priority=priority)
    assert task.payload == payload
    assert task.priority == priority
    assert task.status == expected_status
    assert task.id is not None
    assert isinstance(task.time, datetime)


@pytest.mark.parametrize("invalid_priority", [0, 11, -5, 100, 3.14, "5", None])
def test_invalid_priorities(invalid_priority):
    with pytest.raises((TaskPriorityError, TypeError)):
        Task(payload="Test", priority=invalid_priority)  # type: ignore