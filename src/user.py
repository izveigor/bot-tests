"""Модуль для работы с базой данных redis.

Классы:
    _User - закрытый класс (одиночка) для работы с пользовательскими данными.
Экземпляры классов:
    User - экземпляр класс для работы с пользовательскими данными.ф
"""
from typing import Union

import redis

from src.constants import REDIS_SETTINGS
from src.singleton import Singleton


class _User(metaclass=Singleton):
    """Класс для получения, присваивания или удаления данных пользователей.

    Класс использует базу данных redis для временных записей, хранящех в
    себе информацию про состояние теста для конкретного пользователя.
    """

    def __init__(self) -> None:
        self.redis_ = redis.StrictRedis(**REDIS_SETTINGS)

    def get(self, from_user_id: int, field: str) -> str:
        """Возвращает значение поля по его названию и по пользовательскому id.

        Аргументы:
            from_user_id - пользовательский id
            field - название поля
        Возвращает:
            значение поля, извлеченное из redis
        """
        user_information = self.redis_.hgetall(str(from_user_id))
        user_field = user_information.get(field)
        if user_field is None:
            raise ValueError()

        return str(user_field)

    def set(self, from_user_id: int, **kwargs: Union[str, int]) -> None:
        """Устанавливает значение поля по его названию и по пользовательскому id.

        Аргументы:
            from_user_id - пользовательский id
            **kwargs - (название поля)-(значение)
        Возвращает: None
        """
        self.redis_.hset(
            str(from_user_id),
            mapping=kwargs,  # type: ignore
        )

    def delete(self, from_user_id: int, *args: str) -> None:
        """Удаляет значение поля по его названию и по пользовательскому id.

        Аргументы:
            from_user_id - пользовательский id
            *args - названия полей
        Возвращает: None
        """
        for arg in args:
            self.redis_.hdel(
                str(from_user_id),
                arg,
            )

    def get_tests_with_numbers(self, from_user_id: int) -> list[dict[str, str]]:
        return sorted(
            [
                self.redis_.hgetall(name)
                for name in self.redis_.lrange(str(from_user_id) + "_tests", 0, -1)
            ],
            key=lambda x: list(x.values()),
        )

    def get_tests(self, from_user_id: int) -> list[str]:
        return sorted(
            [
                list(self.redis_.hgetall(name).values())[0]
                for name in self.redis_.lrange(str(from_user_id) + "_tests", 0, -1)
            ]
        )

    def add_test(self, from_user_id: int, number: int, name: str) -> None:
        """Добавляет название теста в список тестов пользователя.

        Аргументы:
            from_user_id - пользовательский id
            number - номер директории, где хранится пользовательский тест
            name - название теста
        Возвращает: None
        """
        hset_name = str(from_user_id) + ":" + str(name)
        if name not in self.get_tests(from_user_id):
            self.redis_.hset(
                hset_name,
                mapping={
                    str(number): name,
                },
            )
            self.redis_.lpush(str(from_user_id) + "_tests", hset_name)

    def delete_test(self, from_user_id: int, name: str) -> None:
        """Удаляет тест из списка тестов пользователя.

        Аргументы:
            from_user_id - пользовательский id
            name - название теста
        Возвращает: None
        """
        hset_name = str(from_user_id) + ":" + str(name)
        self.redis_.lrem(str(from_user_id) + "_tests", 1, hset_name)
        self.redis_.delete(hset_name)


User = _User()
