"""Модуль, содержащий в себе метакласс "Одиночку".

Метаклассы:
    Singleton - метакласс, пременив который у класса возможен только один экземпляр.
"""


from typing import Any


class Singleton(type):
    """
    Метакласс "Одиночка".

    https://ru.wikipedia.org/wiki/%D0%9E%D0%B4%D0%B8%D0%BD%D0%BE%D1%87%D0%BA%D0%B0_(%D1%88%D0%B0%D0%B1%D0%BB%D0%BE%D0%BD_%D0%BF%D1%80%D0%BE%D0%B5%D0%BA%D1%82%D0%B8%D1%80%D0%BE%D0%B2%D0%B0%D0%BD%D0%B8%D1%8F)#Python
    """

    _instances: dict[type, object] = {}

    def __call__(cls, *args: Any, **kwargs: Any) -> object:
        """Вызывается при вызове любого метода класса.

        Возвращает экземпляр класса, если он уже существует, либо сохраняет его.
        Аргументы:
            cls - класс
            *args - позиционные аргументы метода класса
            **kwargs - именнованные аргументы метода класса
        Возвращает: экземпляр класса
        """
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]
