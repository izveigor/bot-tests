"""Модуль для работы с тестами.

Классы:
    Test - открытый класс, содержащий данные и методы для работы над тестами.
"""

from typing import Any, Optional, Union

from telegram import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove

from .bot import bot
from .question import Question
from .user import User


class Test:
    """Класс, экземпляр которого представляет из себя тест.

    Может воспроизводить описание теста,
    Атрибуты:
        command - команда, с помощью которой вызывается тест
        name - название теста
        description - описание теста
        questions - вопросы теста
        result_explanation - объяснение результата теста
    """

    _command: str
    _name: str
    _description: Union[str, dict[str, Any]]
    _questions: list[Question]
    _result_explanation: dict[int, Any]

    def __init__(
        self,
        command: str,
        name: str,
        description: Optional[Union[str, dict[str, Any]]],
        questions: list[Question],
        result_explanation: Optional[dict[str, Any]],
    ):
        """Присваивает и корректирует основные поля теста.

        Аргументы:
            command - команда теста
            name - название теста
            description - описание теста
            questions - вопросы теста
            result_explanation - объяснение результата теста
        Возвращает: None
        """
        self._command = command
        self._name = name
        self._description = description or "Описание отсутствует."
        self._questions = questions

        # Если объяснение результата присутствует, то сортируем
        # ключи в порядке возрастания, иначе возвращаем {}
        self._result_explanation = (
            {
                int(key): value
                for key, value in sorted(
                    result_explanation.items(), key=lambda item: item[0]
                )
            }
            if result_explanation
            else {}
        )

    # Только для чтения
    command = property(lambda self: self._command)
    name = property(lambda self: self._name)
    description = property(lambda self: self._description)
    questions = property(lambda self: self._questions)
    result_explanation = property(lambda self: self._result_explanation)

    async def check(
        self, from_user_id: int, answer: Union[str, int, list[int]]
    ) -> None:
        """Проверяет ответ на текущий вопрос теста.

        Аргументы:
            from_user_id - пользовательский id
            answer - ответ пользователя на текущий вопрос теста
        Возвращает: None
        """
        question_number = int(User.get(from_user_id, "question_index"))
        await self._questions[question_number].check(from_user_id, answer)
        if len(self._questions) == question_number + 1:
            await self._finish(from_user_id)
        else:
            await self._questions[question_number + 1].__call__(from_user_id)

    async def see(self, from_user_id: int) -> None:
        """Возвращает название и описание теста пользователю.

        Дает возможность начать тест.
        Аргументы:
            from_user_id - пользовательский id
        Возвращает: None
        """
        User.set(from_user_id, checked=self.command)
        markup = ReplyKeyboardMarkup(
            [[KeyboardButton("/start_test")]], resize_keyboard=True
        )
        if isinstance(self._description, str):
            await bot.send_message(
                from_user_id,
                "Название: " + self._name + "\nОписание:\n" + self._description,
                reply_markup=markup,
            )
        else:
            url: Optional[str] = self._description.get("url")
            text: Optional[str] = self._description.get("text")
            if not text:
                text = "Описание отсутствует."

            if url:
                await bot.send_photo(
                    from_user_id,
                    url,
                    caption="Название: " + self._name + "\nОписание:\n" + text,
                    reply_markup=markup,
                )
            else:
                await bot.send_message(
                    from_user_id,
                    "Название: " + self._name + "\nОписание:\n" + text,
                    reply_markup=markup,
                )

    async def start(self, from_user_id: int) -> None:
        """Начинает тест.

        Отправляет описание первого вопроса теста.
        Аргументы:
            from_user_id - пользовательский id
        Возвращает: None
        """
        User.delete(from_user_id, "checked")
        User.set(from_user_id, active_test=self._command)
        User.set(from_user_id, question_index=0)
        User.set(from_user_id, right_answers_number=0)
        await bot.send_message(
            from_user_id,
            "Тест начался!",
            reply_markup=ReplyKeyboardRemove(selective=False),
        )
        await self._questions[0].__call__(from_user_id)

    async def stop(self, from_user_id: int) -> None:
        """Преждевременно останавливает тест.

        Аргументы:
            from_user_id - пользовательский id
        Возвращает: None
        """
        await self._finish(from_user_id, is_stop=True)

    async def _finish(self, from_user_id: int, is_stop: bool = False) -> None:
        """Заканчивает тест.

        Аргументы:
            from_user_id - пользовательский id
            is_stop - если True, то отправляет сообщение о пропущенных вопросах
        Возвращает: None
        """
        right_answers_number = int(User.get(from_user_id, "right_answers_number"))
        message = ""

        # Если тест преждевременно остановили
        if is_stop:
            answered_questions = int(User.get(from_user_id, "question_index")) + 1
            skipped_questions = len(self._questions) - answered_questions + 1

            if skipped_questions == 1:
                message += f"Вы преждевременно закончили тест, пропустив {skipped_questions} вопрос.\n"
            elif skipped_questions < 5:
                message += f"Вы преждевременно закончили тест, пропустив {skipped_questions} вопроса.\n"
            else:
                message += f"Вы преждевременно закончили тест, пропустив {skipped_questions} вопросов.\n"

        if right_answers_number == 1:
            message += f"Вы ответили на {right_answers_number} вопрос из {len(self._questions)} ({round(right_answers_number / len(self._questions), 4) * 100}%).\n"
        elif 1 < right_answers_number < 5:
            message += f"Вы ответили на {right_answers_number} вопроса из {len(self._questions)} ({round(right_answers_number / len(self._questions), 4) * 100}%).\n"
        else:
            message += f"Вы ответили на {right_answers_number} вопросов из {len(self._questions)} ({round(right_answers_number / len(self._questions), 4) * 100}%).\n"

        message += "Объяснение результата:\n"

        User.delete(from_user_id, "active_test")
        User.delete(from_user_id, "question_index")
        User.delete(from_user_id, "right_answers_number")

        if not self._result_explanation:
            await bot.send_message(
                from_user_id, message + "Объяснение результата отсутствует."
            )
            return

        # Ищем промежуток объяснения ответа.
        result_explanation_keys = list(self._result_explanation.keys())
        for i in range(len(result_explanation_keys)):
            if right_answers_number < result_explanation_keys[i]:
                break

        if right_answers_number > result_explanation_keys[i]:
            result_message = self._result_explanation[
                result_explanation_keys[len(result_explanation_keys) - 1]
            ]
        elif right_answers_number == result_explanation_keys[i]:
            result_message = self._result_explanation[right_answers_number]
        else:
            if i == 0:
                if right_answers_number < result_explanation_keys[i]:
                    result_message = "Объяснение результата отсутствует."
                else:
                    result_message = self._result_explanation[
                        result_explanation_keys[0]
                    ]
            else:
                result_message = self._result_explanation[
                    result_explanation_keys[i - 1]
                ]

        if isinstance(result_message, str):
            await bot.send_message(from_user_id, message + result_message)
        else:
            url = result_message.get("url")
            text = result_message.get("text")

            if url:
                await bot.send_photo(from_user_id, url, caption=message + text)
            elif text:
                await bot.send_message(from_user_id, message + text)
            else:
                await bot.send_message(
                    from_user_id, message + "Объяснение результата отсутствует."
                )

    def __eq__(self, other: object) -> bool:
        """Сравнивает тесты по команде (знак ==).

        Аргументы:
            other - другой тест
        """
        if not isinstance(other, Test):
            return NotImplemented
        return bool(self.command == other.command)

    def __le__(self, other: object) -> bool:
        """Сравнивает тесты по команде (знак <=).

        Аргументы:
            other - другой тест
        """
        if not isinstance(other, Test):
            return NotImplemented
        return bool(self.command <= other.command)

    def __lt__(self, other: object) -> bool:
        """Сравнивает тесты по команде (знак <).

        Аргументы:
            other - другой тест
        """
        if not isinstance(other, Test):
            return NotImplemented
        return bool(self.command < other.command)

    def __ge__(self, other: object) -> bool:
        """Сравнивает тесты по команде (знак >=).

        Аргументы:
            other - другой тест
        """
        if not isinstance(other, Test):
            return NotImplemented
        return bool(self.command >= other.command)

    def __gt__(self, other: object) -> bool:
        """Сравнивает тесты по команде (знак >).

        Аргументы:
            other - другой тест
        """
        if not isinstance(other, Test):
            return NotImplemented
        return bool(self.command > other.command)
