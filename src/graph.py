import asyncio
import json
from typing import Any, Optional

from telegram import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove

from . import handlers, validate
from .bot import bot
from .builder import BuilderTest
from .user import User


class State:
    _current: int
    _next_: list[dict[str, int | str]]
    _field: str
    _message: str
    _validation: Any
    _handler: Any

    def __init__(
        self,
        current: int,
        next_: list[dict[str, int | str]],
        field: str,
        message: str,
        validation: Optional[Any],
        handler: Any,
    ):
        self._current = current
        self._next_ = next_
        self._field = field
        self._message = message
        self._validation = validation
        self._handler = handler

    async def send(self, from_user_id: int) -> None:
        message = self._message
        state = User.get(from_user_id, "state")
        file_content: dict[str, Any]
        if state == "10":
            jsondata = User.get(from_user_id, "jsondata")
            file_content = json.loads(jsondata)
            type_ = file_content["questions"][len(file_content["questions"]) - 1][
                "widget"
            ]["type"]
            if type_ == "input":
                message += " (Для вашего типа пользовательского интерфейса введите любую строку)."
            elif type_ == "button":
                message += (
                    " (Для вашего типа пользовательского интерфейса введите число)."
                )
            elif type_ == "checkbox":
                message += ' (Для вашего типа пользовательского интерфейса введите числа, разделенные знаком "-" (Например: 1-3)).'
        elif state == "13" or state == "14":
            jsondata = User.get(from_user_id, "jsondata")
            file_content = json.loads(jsondata)
            if (
                len(
                    file_content["questions"][len(file_content["questions"]) - 1][
                        "widget"
                    ]["body"]
                )
                == 4
            ):
                User.set(from_user_id, state=10)
                await bot.send_message(
                    chat_id=from_user_id,
                    text="Вы достигли лимита по созданию кнопок.",
                )
                return await STATES[10].send(from_user_id)

        if len(self._next_) == 1:
            await bot.send_message(
                chat_id=from_user_id,
                text=message,
            )
        else:
            keyboard = [[KeyboardButton(data["message"]) for data in self._next_]]
            markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
            await bot.send_message(
                chat_id=from_user_id,
                text=self._message,
                reply_markup=markup,
            )
        if state == "22":
            User.delete(from_user_id, "state")
            await asyncio.gather(
                BuilderTest().create_test(
                    from_user_id,
                    json.loads(User.get(from_user_id, "jsondata")),
                )
            )

    async def handle(self, from_user_id: int, message: str) -> None:
        if message == "/stop":
            User.delete(from_user_id, "state")
            User.delete(from_user_id, "jsondata")
            await bot.send_message(
                chat_id=from_user_id,
                text="Вы остановили процесс создания теста. Все данные вашего теста были удалены.",
            )
        else:
            fields = self._field.split(".")
            file_content: dict[str, Any]
            try:
                jsondata = User.get(from_user_id, "jsondata")
            except ValueError:
                file_content = {}
            else:
                file_content = json.loads(jsondata)
            if len(self._next_) == 1:
                if self._handler is not None:
                    await self._handler(
                        file_content,
                        from_user_id,
                        fields,
                        self._validation,
                        message,
                        self._next_,
                    )
            else:
                if self._handler is not None:
                    await self._handler(
                        file_content,
                        from_user_id,
                        fields,
                        self._validation,
                        message,
                        self._next_,
                    )

                for next_state in self._next_:
                    if message == next_state["message"]:
                        User.set(from_user_id, state=next_state["state"])
                        await bot.send_message(
                            chat_id=from_user_id,
                            text=f'Вы нажали на кнопку "{message}".',
                            reply_markup=ReplyKeyboardRemove(selective=False),
                        )
                        break
                else:
                    await bot.send_message(
                        chat_id=from_user_id,
                        text="Такой кнопки нет. Отвечайте на вопрос с помощью кнопок.",
                    )

    # Только для чтения
    current = property(lambda self: self._current)
    next_ = property(lambda self: self._next_)
    field = property(lambda self: self._field)
    message = property(lambda self: self._message)
    validation = property(lambda self: self._validation)
    handler = property(lambda self: self._handler)


STATES = [
    State(
        0,
        [{"state": 1, "message": ""}],
        "command",
        "Введите команду теста:",
        validate.is_command_right,
        handlers.command_handler,
    ),
    State(
        1,
        [{"state": 2, "message": ""}],
        "name",
        "Введите имя теста:",
        validate.is_name_right,
        handlers.name_handler,
    ),
    State(
        2,
        [{"state": 3, "message": "Да"}, {"state": 4, "message": "Нет"}],
        "",
        "Добавить описание теста?",
        None,
        None,
    ),
    State(
        3,
        [{"state": 5, "message": ""}],
        "description.text",
        "Введите текст описания теста:",
        validate.is_description_right,
        handlers.description_handler,
    ),
    State(
        4,
        [{"state": 7, "message": ""}],
        "questions.body.text",
        "Введите текст вопроса:",
        validate.is_question_body_right,
        handlers.body_handler,
    ),
    State(
        5,
        [{"state": 6, "message": "Да"}, {"state": 4, "message": "Нет"}],
        "",
        "Добавить рисунок в описание теста?",
        None,
        None,
    ),
    State(
        6,
        [{"state": 4, "message": ""}],
        "description.url",
        "Введите url рисунка:",
        validate.is_description_right,
        handlers.description_handler,
    ),
    State(
        7,
        [{"state": 8, "message": "Да"}, {"state": 9, "message": "Нет"}],
        "",
        "Добавить рисунок в тело вопроса?",
        None,
        None,
    ),
    State(
        8,
        [{"state": 9, "message": ""}],
        "questions.body.url",
        "Введите url рисунка:",
        validate.is_question_body_right,
        handlers.body_handler,
    ),
    State(
        9,
        [
            {"state": 10, "message": "input"},
            {"state": 11, "message": "button"},
            {"state": 12, "message": "checkbox"},
        ],
        "questions.widget.type",
        "Выберите тип пользовательского интерфейса.",
        validate.is_type_right,
        handlers.type_handler,
    ),
    State(
        10,
        [{"state": 15, "message": ""}],
        "questions.answer",
        "Введите ответ на вопрос:",
        validate.is_answer_right,
        handlers.answer_handler,
    ),
    State(
        11,
        [{"state": 13, "message": ""}],
        "questions.widget.body",
        "Введите текст кнопки",
        validate.is_widget_body_right,
        handlers.widget_handler,
    ),
    State(
        12,
        [{"state": 14, "message": ""}],
        "questions.widget.body",
        "Введите текст флаговой кнопки",
        validate.is_widget_body_right,
        handlers.widget_handler,
    ),
    State(
        13,
        [{"state": 11, "message": "Да"}, {"state": 10, "message": "Нет"}],
        "",
        "Хотите добавить еще одну кнопку (максимум - 4 кнопки)?",
        None,
        None,
    ),
    State(
        14,
        [{"state": 12, "message": "Да"}, {"state": 10, "message": "Нет"}],
        "",
        "Хотите добавить еще одну флаговую кнопку (максимум - 4 флаговой кнопки)?",
        None,
        None,
    ),
    State(
        15,
        [{"state": 16, "message": "Да"}, {"state": 17, "message": "Нет"}],
        "",
        "Хотите добавить объяснение ответа?",
        None,
        None,
    ),
    State(
        16,
        [{"state": 18, "message": ""}],
        "questions.answer_explanation.text",
        "Введите текст объяснения результата:",
        validate.is_answer_explanation_right,
        handlers.body_handler,
    ),
    State(
        17,
        [{"state": 4, "message": "Да"}, {"state": 20, "message": "Нет"}],
        "",
        "Хотите добавить еще один вопрос?",
        None,
        None,
    ),
    State(
        18,
        [{"state": 19, "message": "Да"}, {"state": 17, "message": "Нет"}],
        "",
        "Хотите добавить рисунок в объяснение результата?",
        None,
        None,
    ),
    State(
        19,
        [{"state": 17, "message": ""}],
        "questions.answer_explanation.url",
        "Введите url рисунка:",
        validate.is_answer_explanation_right,
        handlers.body_handler,
    ),
    State(
        20,
        [{"state": 21, "message": "Да"}, {"state": 22, "message": "Нет"}],
        "",
        "Хотите добавить объяснение результата?",
        None,
        None,
    ),
    State(
        21,
        [{"state": 23, "message": ""}],
        "result_explanation",
        "Введите начало промежутка: (Примечание: начало промежутка - это число правильных ответов. Если вы введете число 2, то объяснение результата будет появляться в тех случаях, если количество правильных ответов больше или равно 2. Однако, если присутствует промежуток, который больше 2 (например, 3), то объяснение промежутка будет появляться от 2 до 3 включительно (после 3 правильных ответов будет появляться промежуток, который определен под числом 3).",
        validate.is_result_explanation_right,
        handlers.result_explanation_handler,
    ),
    State(
        22,
        [],
        "",
        "Создание теста завершено!",
        None,
        None,
    ),
    State(
        23,
        [{"state": 24, "message": "Да"}, {"state": 27, "message": "Нет"}],
        "",
        "Добавить текст объяснения промежутка?",
        None,
        None,
    ),
    State(
        24,
        [{"state": 25, "message": ""}],
        "result_explanation.text",
        "Введите текст объяснения промежутка:",
        validate.is_result_explanation_right,
        handlers.result_explanation_text_handler,
    ),
    State(
        25,
        [{"state": 26, "message": "Да"}, {"state": 27, "message": "Нет"}],
        "",
        "Добавить рисунок в объяснение промежутка?",
        None,
        None,
    ),
    State(
        26,
        [{"state": 27, "message": ""}],
        "result_explanation.url",
        "Введите url рисунка:",
        validate.is_result_explanation_right,
        handlers.result_explanation_text_handler,
    ),
    State(
        27,
        [{"state": 21, "message": "Да"}, {"state": 22, "message": "Нет"}],
        "",
        "Добавить еще один промежуток?",
        None,
        None,
    ),
]
