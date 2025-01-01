"""
exceptions.py

Модуль, содержащий пользовательские классы исключений.

Этот файл используется для определения специфических исключений, которые
могут возникнуть в приложении, таких как отсутствие файлов или ошибки аргументов.

Классы:
    - ProjectError: Базовый класс для всех исключений в проекте.
    - FileMissingError: Исключение, возникающее при отсутствии файла.
    - InvalidArgumentError: Исключение, возникающее при некорректных аргументах.
    - TimerError: Исключение, связанное с таймером.
"""


class ProjectError(Exception):
    """
    Базовый класс для всех исключений проекта.
    """
    pass


class FileMissingError(ProjectError):
    """
    Исключение, вызываемое при отсутствии файла.
    """
    def __init__(self, file_name: str):
        self.file_name = file_name
        super().__init__(f"Файл '{file_name}' не найден. Проверьте наличие файла.")


class InvalidArgumentError(ProjectError):
    """
    Исключение, вызываемое при передаче некорректных аргументов.
    """
    def __init__(self, argument_name: str, expected_type: type):
        self.argument_name = argument_name
        self.expected_type = expected_type
        super().__init__(f"Аргумент '{argument_name}' должен быть типа {expected_type}.")


class TimerError(ProjectError):
    """
    Исключение, связанное с ошибками таймера.
    """
    def __init__(self, message: str):
        super().__init__(f"Ошибка таймера: {message}")