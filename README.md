#  Реализация расширенной модели задачи ( Task ) в рамках платформы обработки задач — Лабораторная работа №2

## Описание

Реализация модели задачи ( Task ) в рамках платформы обработки задач с корректной инкапсуляцией и валидацией состояния.

## Основной функционал:

### Система приема и обработки задач
- Duck typing через Protocol: источники задач не связаны наследованием
- Единый контракт: все источники реализуют get_tasks() -> Iterator[Task]
- Ленивая загрузка через Iterator
- Runtime-проверка: isinstance() с @runtime_checkable
- Поддержка 3 типов источников: файл, генератор, API-заглушка
- Расширяемость: возможность добавления новых источников без изменения существующего кода

### Модель  задачи ( Task )
- Пользовательские дескрипторы: валидация атрибутов через ValidPayload, ValidPriority, ValidStatus
- Data descriptors: __get__ и __set__ для полного контроля доступа
- Read-only свойства: id, time, status защищены через @property
- Вычисляемые свойства: is_ready, is_active, is_done, age
- Специализированные исключения: TaskPayloadError, TaskPriorityError, TaskStatusError
- Инкапсуляция: разделение публичного API (task.payload) и внутреннего состояния (self._payload)
- Валидация инвариантов: предотвращение некорректных состояний объекта
- Покрытие тестами
- Логирование: централизованное логирование всех операций валидации

## Структура репозитория
```
python-lab-2.1/
│
├── task.py              # Модель Task с дескрипторами и property
├── descriptors.py       # Пользовательские дескрипторы (ValidPayload, ValidPriority, ValidStatus)
├── exceptions.py        # Иерархия специализированных исключений
├── system.py            # Источники задач (Generator, API, File)
├── main.py              # Точка входа для демонстрации
├── tests.py             # Тесты
├── requirements.txt     # Зависимости
├── README.md            # Описание
```

## Установка и запуск

### 1. Требования
- Python 3.10+ (для синтаксиса str | int)
- pytest 7.0.0+

### 2. Установка зависимостей
```
pip install -r requirements.txt
```
### 3. Запуск демонстрации
```
python main.py
```
### 4. Запуск тестов
```
pytest tests.py
```

## Демонстрация работы
```
2026-03-29 02:56:10,829 - INFO - Demonstration started.
2026-03-29 02:56:10,829 - INFO - 
Task class demonstration
2026-03-29 02:56:10,829 - INFO - Task created: id=ad8eeb19-d307-4d71-a760-15bfbc077bcb
2026-03-29 02:56:10,830 - INFO - Payload: Demo user task
2026-03-29 02:56:10,830 - INFO - Priority: 8
2026-03-29 02:56:10,830 - INFO - Status: new
2026-03-29 02:56:10,830 - INFO - Created at: 2026-03-29 02:56:10.829575
2026-03-29 02:56:10,830 - INFO - Safety check: trying to change task ID
Access denied: property 'id' of 'Task' object has no setter
2026-03-29 02:56:10,831 - INFO - payload was updated: Updated payload
2026-03-29 02:56:10,832 - INFO - age = 0.002995 sec
2026-03-29 02:56:10,832 - INFO -
Returning task from sources demonstration
2026-03-29 02:56:10,832 - INFO - Generating 2 tasks
2026-03-29 02:56:10,832 - INFO - 1. Task(id='aa436803-2d90-499f-8f1e-a3dea3b0a008', payload='Task type: gen, Task number: 0', priority=5, status='new')
2026-03-29 02:56:10,832 - INFO - 2. Task(id='aa2bed9d-6843-4c23-befc-ea5c61d8ef5e', payload='Task type: gen, Task number: 1', priority=10, status='new')        
2026-03-29 02:56:10,833 - INFO -

2026-03-29 02:56:10,856 - INFO - Demonstration completed.
```
