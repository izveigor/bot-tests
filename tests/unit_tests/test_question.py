from typing import Any, Optional, Union
from unittest.mock import AsyncMock, Mock, call, patch

import pytest
from telegram import InlineKeyboardButton, KeyboardButton, ReplyKeyboardRemove

from src.question import Question


class TestQuestion:
    @pytest.mark.parametrize(
        ("init_arguments", "markup_arguments"),
        [
            (
                {
                    "body": 'Нажми на кнопку "Yes".',
                    "widget": {
                        "type": "button",
                        "body": [
                            "Yes",
                            "No",
                        ],
                    },
                    "answer": "Yes",
                    "answer_explanation": 'Ты нажал кнопку "Yes".',
                },
                {"keyboard": [[{"text": "Yes"}, {"text": "No"}]]},
            ),
            (
                {
                    "body": "Выбери кнопки",
                    "widget": {
                        "type": "checkbox",
                        "body": [
                            "1",
                            "2",
                            "3",
                            "4",
                        ],
                    },
                    "answer": [1, 2],
                    "answer_explanation": "Ты выбрал 1 и 2, это правильно!",
                },
                {
                    "keyboard": [
                        [{"text": "1"}, {"text": "2"}],
                        [{"text": "3"}, {"text": "4"}],
                        [{"text": "Ответить"}],
                    ],
                },
            ),
        ],
    )
    def test__init__(
        self, init_arguments: dict[str, Any], markup_arguments: dict[str, Any]
    ) -> None:
        question = Question(**init_arguments)

        assert question._body == init_arguments["body"]
        assert question._answer == init_arguments["answer"]
        assert question._answer_explanation == init_arguments["answer_explanation"]
        assert question._widget_type == init_arguments["widget"]["type"]
        assert question._widget_body == init_arguments["widget"]["body"]

        if question._widget_type != "input":
            if question._widget_type == "button" and isinstance(
                question._markup, KeyboardButton
            ):
                for i in range(len(question._markup.keyboard)):
                    for j in range(len(question._markup.keyboard[i])):
                        assert (
                            question._markup.keyboard[i][j]["text"]
                            == markup_arguments["keyboard"][i][j]["text"]
                        )
            elif question._widget_type == "checkbox" and isinstance(
                question._markup, InlineKeyboardButton
            ):
                for i in range(len(question._markup.inline_keyboard)):
                    for j in range(len(question._markup.inline_keyboard[i])):
                        assert (
                            question._markup.inline_keyboard[i][j]["text"]
                            == markup_arguments["keyboard"][i][j]["text"]
                        )

    @pytest.mark.parametrize(
        (
            "answer",
            "self_answer",
            "widget_type",
            "widget_body",
            "self_answer_explanation",
            "patch_",
            "message",
            "get_arguments",
            "get_return",
            "set_arguments",
        ),
        [
            (
                "Правильный ответ",
                "Правильный ответ",
                "input",
                None,
                "Объяснение ответа отсутствует.",
                "src.question.bot.send_message",
                call(
                    chat_id=-1,
                    text='Правильно ✅\nВаш ответ: "Правильный ответ"\nПравильный ответ: "Правильный ответ"\nОбъяснение ответа:\nОбъяснение ответа отсутствует.',
                    reply_markup=None,
                ),
                [call(-1, "right_answers_number"), call(-1, "question_index")],
                [2, 1],
                [call(-1, right_answers_number=3), call(-1, question_index=2)],
            ),
            (
                "Неправильный ответ",
                "Правильный ответ",
                "input",
                None,
                "Объяснение ответа отсутствует.",
                "src.question.bot.send_message",
                call(
                    chat_id=-1,
                    text='Неправильно ❌\nВаш ответ: "Неправильный ответ"\nПравильный ответ: "Правильный ответ"\nОбъяснение ответа:\nОбъяснение ответа отсутствует.',
                    reply_markup=None,
                ),
                [call(-1, "question_index")],
                [2],
                [call(-1, question_index=3)],
            ),
            (
                "Yes",
                1,
                "button",
                ["Yes", "No"],
                'Надо было нажать кнопку "Yes".',
                "src.question.bot.send_message",
                call(
                    chat_id=-1,
                    text='Правильно ✅\nВаш ответ: "Yes"\nПравильный ответ: "Yes"\nОбъяснение ответа:\nНадо было нажать кнопку "Yes".',
                    reply_markup=ReplyKeyboardRemove,
                ),
                [call(-1, "right_answers_number"), call(-1, "question_index")],
                [2, 1],
                [call(-1, right_answers_number=3), call(-1, question_index=2)],
            ),
            (
                "No",
                1,
                "button",
                ["Yes", "No"],
                {"text": 'Надо было нажать кнопку "Yes".'},
                "src.question.bot.send_message",
                call(
                    chat_id=-1,
                    text='Неправильно ❌\nВаш ответ: "No"\nПравильный ответ: "Yes"\nОбъяснение ответа:\nНадо было нажать кнопку "Yes".',
                    reply_markup=ReplyKeyboardRemove,
                ),
                [call(-1, "question_index")],
                [2],
                [call(-1, question_index=3)],
            ),
            (
                [1, 3],
                [1, 3],
                "checkbox",
                ["1", "2", "3", "4"],
                {"url": "smile.png", "text": 'Надо было нажать кнопку "Yes".'},
                "src.question.bot.send_photo",
                call(
                    chat_id=-1,
                    photo="smile.png",
                    caption='Правильно ✅\nВаш ответ: "1, 3"\nПравильный ответ: "1, 3"\nОбъяснение ответа:\nНадо было нажать кнопку "Yes".',
                    reply_markup=None,
                ),
                [call(-1, "right_answers_number"), call(-1, "question_index")],
                [2, 1],
                [call(-1, right_answers_number=3), call(-1, question_index=2)],
            ),
            (
                [1, 2],
                [1, 3],
                "checkbox",
                ["1", "2", "3", "4"],
                {"url": "smile.png", "text": 'Надо было нажать кнопку "Yes".'},
                "src.question.bot.send_photo",
                call(
                    chat_id=-1,
                    photo="smile.png",
                    caption='Неправильно ❌\nВаш ответ: "1, 2"\nПравильный ответ: "1, 3"\nОбъяснение ответа:\nНадо было нажать кнопку "Yes".',
                    reply_markup=None,
                ),
                [call(-1, "question_index")],
                [2],
                [call(-1, question_index=3)],
            ),
        ],
    )
    @patch("src.question.User.get")
    @patch("src.question.User.set")
    @patch("src.question.Question.__init__", return_value=None)
    @pytest.mark.asyncio
    async def test_check(
        self,
        mock__init__: Mock,
        mock_user_set: Mock,
        mock_user_get: Mock,
        answer: Union[str, list[int]],
        self_answer: Union[str, int, list[int]],
        widget_type: str,
        widget_body: Optional[list[str]],
        self_answer_explanation: Optional[Union[str, dict[str, str]]],
        patch_: str,
        message: Any,
        get_arguments: Any,
        get_return: list[int],
        set_arguments: Any,
    ) -> None:
        with patch(patch_, new_callable=AsyncMock) as mock_bot_action:
            mock_user_get.side_effect = get_return
            question = Question("", {}, "", None)
            question._widget_type = widget_type
            if widget_body:
                question._widget_body = widget_body
            question._answer = self_answer
            question._answer_explanation = self_answer_explanation
            await question.check(-1, answer)
            mock_user_get.assert_has_calls(get_arguments)
            mock_user_set.assert_has_calls(set_arguments)

            _, mock_kwargs = mock_bot_action.call_args_list[0]
            message_kwargs = message.kwargs
            reply_markup = mock_kwargs.pop("reply_markup")
            message_kwargs.pop("reply_markup")
            assert mock_kwargs == message_kwargs
            if mock_kwargs.get("reply_markup") is not None:
                assert isinstance(reply_markup, message.kwargs["reply_markup"])
            else:
                assert message.kwargs.get("reply_markup") is None

    @pytest.mark.parametrize(
        ("body", "patch_", "mock_call"),
        [
            (
                "В каком году родился А.С.Пушкин?",
                "src.question.bot.send_message",
                call(
                    chat_id=-1,
                    text="В каком году родился А.С.Пушкин?",
                    reply_markup=None,
                ),
            ),
            (
                {"text": "В каком году родился А.С.Пушкин?"},
                "src.question.bot.send_message",
                call(
                    chat_id=-1,
                    text="В каком году родился А.С.Пушкин?",
                    reply_markup=None,
                ),
            ),
            (
                {"url": "Pushkin.png", "text": "В каком году родился А.С.Пушкин?"},
                "src.question.bot.send_photo",
                call(
                    chat_id=-1,
                    photo="Pushkin.png",
                    caption="В каком году родился А.С.Пушкин?",
                    reply_markup=None,
                ),
            ),
        ],
    )
    @pytest.mark.asyncio
    async def test__call__(
        self, body: Union[str, dict[str, str]], patch_: str, mock_call: Any
    ) -> None:
        with patch(patch_, new_callable=AsyncMock) as mock_bot_action, patch(
            "src.question.Question.__init__"
        ) as mock__init__:
            mock__init__.return_value = None
            question = Question("", {}, "", None)
            question._body = body
            question._markup = None
            await question(-1)
            mock_bot_action.assert_has_calls([mock_call])
