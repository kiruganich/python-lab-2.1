"""
Исключения для модели задачи.

"""


class TaskValidationError(Exception):
    """
    Базовое исключение для ошибок валидации задачи.

    """
    pass


class TaskIDError(TaskValidationError):
    """Ошибка валидации идентификатора задачи."""
    pass


class TaskPayloadError(TaskValidationError):
    """Ошибка валидации описания задачи."""
    pass


class TaskPriorityError(TaskValidationError):
    """Ошибка валидации приоритета задачи."""
    pass


class TaskStatusError(TaskValidationError):
    """Ошибка валидации статуса задачи."""
    pass



class TaskSourceValidationError(Exception):
    """
    Базовое исключение для ошибок валидации источников

    """
    pass