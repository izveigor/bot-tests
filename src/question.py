"""Модуль для работы с вопросами теста.

Классы:
    Question - открытый класс, содержащий данные и методы для работы над вопросами теста.
"""


from typing import Optional, Union

from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
)

from src.user import User

from .bot import bot


class Question:
    """Класс, экземпляр которого представляет из себя вопрос.

    Может воспроизводить описание вопроса и проверяет ответ пользователя на правильность.
    Атрибуты:
        body - тело вопроса
        answer - ответ на вопрос
        widget_type - тип элемента интерфейса
        widget_body - тело элемента интерфейса
        answer_explanation - объяснение ответа
        markup - элемент интерфейса Телеграма
    """

    _body: Union[str, dict[str, str]]
    _answer: Union[str, int, list[int]]
    _widget_type: str
    _widget_body: list[str]
    _answer_explanation: Optional[Union[str, dict[str, str]]]
    _markup: Optional[Union[InlineKeyboardButton, KeyboardButton]]

    def __init__(
        self,
        body: Union[str, dict[str, str]],
        widget: Optional[dict[str, Union[str, list[str]]]],
        answer: Union[str, int, list[int]],
        answer_explanation: Optional[Union[str, dict[str, str]]],
    ) -> None:
        """Присваивает и корректирует основные поля вопроса.

        Аргументы:
            body - тело вопроса
            widget - элемент интерфейса вопроса
            answer - ответ на вопрос
            answer_explanation - объяснение ответа на вопрос
        Возвращает: None
        """
        self._body = body
        self._answer = answer

        self._answer_explanation = (
            answer_explanation or "Объяснение ответа отсутствует."
        )

        widget_type = widget.get("type", "input") if widget else "input"
        widget_body = widget.get("body") if widget else []
        markup = None

        if isinstance(widget_type, str):
            self._widget_type = widget_type

        if isinstance(widget_body, list):
            self._widget_body = widget_body

            if self._widget_type == "button":
                keyboard = [
                    [KeyboardButton(button) for button in self._widget_body[:2]],
                    [KeyboardButton(button) for button in self._widget_body[2:]],
                ]

                markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
            elif self._widget_type == "checkbox":
                keyboard = [
                    [
                        InlineKeyboardButton(button, callback_data=counter)
                        for counter, button in enumerate(self._widget_body[:2], start=1)
                    ],
                    [
                        InlineKeyboardButton(button, callback_data=counter)
                        for counter, button in enumerate(self._widget_body[2:], start=3)
                    ],
                    [InlineKeyboardButton("Ответить", callback_data="Ответить")],
                ]

                markup = InlineKeyboardMarkup(keyboard)

        self._markup = markup

    # Только для чтения
    body = property(lambda self: self._body)
    answer = property(lambda self: self._answer)
    answer_epxlanation = property(lambda self: self._answer_explanation)
    widget_type = property(lambda self: self._widget_type)
    widget_body = property(lambda self: self._widget_body)
    markup = property(lambda self: self._markup)

    async def __call__(self, from_user_id: int) -> None:
        """Отправляет пользователю описание вопроса.

        Аргументы:
            from_user_id - пользовательский id
        Возвращает: None
        """
        if isinstance(self._body, str):
            await bot.send_message(
                chat_id=from_user_id, text=self._body, reply_markup=self._markup
            )
        else:
            url = self._body.get("url")
            text = self._body.get("text")

            if url:
                await bot.send_photo(
                    chat_id=from_user_id,
                    photo=url,
                    caption=text,
                    reply_markup=self._markup,
                )
            else:
                await bot.send_message(
                    chat_id=from_user_id,
                    text=text,
                    reply_markup=self._markup,
                )

    async def check(
        self,
        from_user_id: int,
        answer: Union[str, int, list[int]],
    ) -> None:
        """Проверяет ответ пользователя.

        После проверки ответа, сообщает пользователю результат, правильный ответ и объяснение ответа.
        Аргументы:
            from_user_id - пользовательский id
            answer - ответ пользователя на вопрос
        Возвращает: None
        """
        markup = None
        if (
            isinstance(answer, str)
            and isinstance(self._answer, str)
            and self._widget_type == "input"
        ):
            if answer == self._answer:
                message = f'Правильно ✅\nВаш ответ: "{answer}"\nПравильный ответ: "{self._answer}"\nОбъяснение ответа:\n'
                User.set(
                    from_user_id,
                    right_answers_number=int(
                        User.get(from_user_id, "right_answers_number")
                    )
                    + 1,
                )
            else:
                message = f'Неправильно ❌\nВаш ответ: "{answer}"\nПравильный ответ: "{self._answer}"\nОбъяснение ответа:\n'
        elif (
            isinstance(answer, str)
            and isinstance(self._answer, int)
            and self._widget_type == "button"
        ):
            markup = ReplyKeyboardRemove(selective=False)
            if answer == self._widget_body[self._answer - 1]:
                message = f'Правильно ✅\nВаш ответ: "{answer}"\nПравильный ответ: "{self._widget_body[self._answer - 1]}"\nОбъяснение ответа:\n'
                User.set(
                    from_user_id,
                    right_answers_number=int(
                        User.get(from_user_id, "right_answers_number")
                    )
                    + 1,
                )
            else:
                message = f'Неправильно ❌\nВаш ответ: "{answer}"\nПравильный ответ: "{self._widget_body[self._answer - 1]}"\nОбъяснение ответа:\n'
        elif isinstance(answer, list) and isinstance(self._answer, list):
            if answer == self._answer:
                message = f'Правильно ✅\nВаш ответ: "{", ".join([self._widget_body[_answer - 1] for _answer in answer])}"\nПравильный ответ: "{", ".join([self._widget_body[_answer - 1] for _answer in self._answer])}"\nОбъяснение ответа:\n'
                User.set(
                    from_user_id,
                    right_answers_number=int(
                        User.get(from_user_id, "right_answers_number")
                    )
                    + 1,
                )
            else:
                message = f'Неправильно ❌\nВаш ответ: "{", ".join([self._widget_body[_answer - 1] for _answer in answer])}"\nПравильный ответ: "{", ".join([self._widget_body[_answer - 1] for _answer in self._answer])}"\nОбъяснение ответа:\n'

        User.set(
            from_user_id,
            question_index=int(User.get(from_user_id, "question_index")) + 1,
        )
        if isinstance(self._answer_explanation, str):
            message += self._answer_explanation
            await bot.send_message(
                chat_id=from_user_id,
                text=message,
                reply_markup=markup,
            )
        elif isinstance(self._answer_explanation, dict):
            url = self._answer_explanation.get("url")
            text = self._answer_explanation["text"]

            if text:
                message += text
            else:
                message += "Объяснение ответа отсутствует."

            if url:
                await bot.send_photo(
                    chat_id=from_user_id,
                    photo=url,
                    reply_markup=markup,
                    caption=message,
                )
            else:
                await bot.send_message(
                    chat_id=from_user_id,
                    text=message,
                    reply_markup=markup,
                )
