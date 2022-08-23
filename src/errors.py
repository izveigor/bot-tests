"""Модуль ошибок.

Классы:
    BotException - открытый класс, наследник Exception.
    BotParseException - открытый класс, наследник BotException.
    BotFilesException - открытый класс, наследник BotException.
"""

from typing import Union


class BotException(Exception):
    """Общий класс ошибок для бота."""

    def __init__(self, errors: list[Union[str, int]], message: str) -> None:
        """Помещает сообщение об ошибки в список errors.

        Аргументы:
            errors - список ошибок
            message - сообщение
        Возвращает: None
        """
        errors.append(message)


class BotParseException(BotException):
    """Вызывается, если json-схема не может быть разобрана."""


class BotFilesException(BotException):
    """Вызывается, если есть проблема с файлами."""
