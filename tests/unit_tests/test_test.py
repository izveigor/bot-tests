from typing import Any, Optional, Union
from unittest.mock import AsyncMock, Mock, call, patch

import pytest
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove

from src.question import Question
from src.test import Test


@patch("src.test.Test.__init__", return_value=None)
@patch("src.test.User.set")
@patch("src.test.User.get")
class TestSee:
    @pytest.mark.parametrize(
        ("description", "patch_", "args", "caption"),
        [
            (
                "Описание теста.",
                "src.test.bot.send_message",
                (-1, "Название: Name\nОписание:\nОписание теста."),
                None,
            ),
            (
                {"text": "Описание теста."},
                "src.test.bot.send_message",
                (-1, "Название: Name\nОписание:\nОписание теста."),
                None,
            ),
            (
                {"url": "photo.png", "text": "Описание теста."},
                "src.test.bot.send_photo",
                (-1, "photo.png"),
                "Название: Name\nОписание:\nОписание теста.",
            ),
        ],
    )
    @pytest.mark.asyncio
    async def test_see(
        self,
        mock_user_get: Mock,
        mock_user_set: Mock,
        mock__init__: Mock,
        description: Union[str, dict[str, str]],
        patch_: str,
        args: tuple[int, str],
        caption: Optional[str],
    ) -> None:
        with patch(patch_, new_callable=AsyncMock) as mock_bot_action:
            test = Test("", "", None, [], None)
            test._description = description
            test._name = "Name"
            test._command = "/test_test"
            await test.see(-1)

            mock_user_set.assert_called_once_with(-1, checked=test._command)
            mock_calls = mock_bot_action.mock_calls[0]

            assert mock_calls.args == args
            if caption:
                assert mock_calls.kwargs["caption"] == caption
            assert isinstance(mock_calls.kwargs["reply_markup"], ReplyKeyboardMarkup)


class TestFinish:
    @pytest.mark.parametrize(
        ("result_explanation", "get_arguments", "is_stop", "patch_", "mock_call"),
        [
            (
                {0: "Плохо", 1: "Средне", 2: "Хорошо"},
                [1],
                False,
                "src.test.bot.send_message",
                call(
                    -1,
                    "Вы ответили на 1 вопрос из 10 (10.0%).\nОбъяснение результата:\nСредне",
                ),
            ),
            (
                {0: "Плохо", 5: "Хорошо"},
                [0],
                False,
                "src.test.bot.send_message",
                call(
                    -1,
                    "Вы ответили на 0 вопросов из 10 (0.0%).\nОбъяснение результата:\nПлохо",
                ),
            ),
            (
                {0: "Плохо", 5: "Хорошо"},
                [2],
                False,
                "src.test.bot.send_message",
                call(
                    -1,
                    "Вы ответили на 2 вопроса из 10 (20.0%).\nОбъяснение результата:\nПлохо",
                ),
            ),
            (
                {0: "Плохо", 5: "Хорошо"},
                [5],
                False,
                "src.test.bot.send_message",
                call(
                    -1,
                    "Вы ответили на 5 вопросов из 10 (50.0%).\nОбъяснение результата:\nХорошо",
                ),
            ),
            (
                {0: "Плохо", 5: "Хорошо"},
                [6],
                False,
                "src.test.bot.send_message",
                call(
                    -1,
                    "Вы ответили на 6 вопросов из 10 (60.0%).\nОбъяснение результата:\nХорошо",
                ),
            ),
            (
                {},
                [2],
                False,
                "src.test.bot.send_message",
                call(
                    -1,
                    "Вы ответили на 2 вопроса из 10 (20.0%).\nОбъяснение результата:\nОбъяснение результата отсутствует.",
                ),
            ),
            (
                None,
                [2],
                False,
                "src.test.bot.send_message",
                call(
                    -1,
                    "Вы ответили на 2 вопроса из 10 (20.0%).\nОбъяснение результата:\nОбъяснение результата отсутствует.",
                ),
            ),
            (
                {2: {}},
                [2],
                False,
                "src.test.bot.send_message",
                call(
                    -1,
                    "Вы ответили на 2 вопроса из 10 (20.0%).\nОбъяснение результата:\nОбъяснение результата отсутствует.",
                ),
            ),
            (
                {0: "Плохо", 1: {"url": "smile.png", "text": "Отлично!"}},
                [1],
                False,
                "src.test.bot.send_photo",
                call(
                    -1,
                    "smile.png",
                    caption="Вы ответили на 1 вопрос из 10 (10.0%).\nОбъяснение результата:\nОтлично!",
                ),
            ),
            (
                {0: {"text": "Плохо"}, 1: "Хорошо"},
                [0],
                False,
                "src.test.bot.send_message",
                call(
                    -1,
                    "Вы ответили на 0 вопросов из 10 (0.0%).\nОбъяснение результата:\nПлохо",
                ),
            ),
            (
                {0: {"text": "Плохо"}, 1: "Хорошо"},
                [0, 5],
                True,
                "src.test.bot.send_message",
                call(
                    -1,
                    "Вы преждевременно закончили тест, пропустив 5 вопросов.\nВы ответили на 0 вопросов из 10 (0.0%).\nОбъяснение результата:\nПлохо",
                ),
            ),
            (
                {0: {"text": "Плохо"}, 1: "Хорошо"},
                [0, 8],
                True,
                "src.test.bot.send_message",
                call(
                    -1,
                    "Вы преждевременно закончили тест, пропустив 2 вопроса.\nВы ответили на 0 вопросов из 10 (0.0%).\nОбъяснение результата:\nПлохо",
                ),
            ),
            (
                {0: {"text": "Плохо"}, 1: "Хорошо"},
                [0, 9],
                True,
                "src.test.bot.send_message",
                call(
                    -1,
                    "Вы преждевременно закончили тест, пропустив 1 вопрос.\nВы ответили на 0 вопросов из 10 (0.0%).\nОбъяснение результата:\nПлохо",
                ),
            ),
        ],
    )
    @patch("src.test.User.delete")
    @patch("src.test.Question.__init__", return_value=None)
    @patch("src.test.Test.__init__", return_value=None)
    @pytest.mark.asyncio
    async def test_finish(
        self,
        mock__init__: Mock,
        mock_question__init__: Mock,
        mock_user_delete: Mock,
        result_explanation: dict[int, str],
        get_arguments: list[int],
        is_stop: bool,
        patch_: str,
        mock_call: Any,
    ) -> None:
        with patch(patch_, new_callable=AsyncMock) as mock_bot_action, patch(
            "src.test.User.get",
        ) as mock_user_get:
            mock_user_get.side_effect = get_arguments

            test = Test("", "", None, [], None)
            test._questions = [Question("", {}, "", None) for i in range(10)]
            test._result_explanation = result_explanation
            await test._finish(-1, is_stop)

            mock_bot_action.assert_has_awaits([mock_call])
            mock_user_delete.assert_has_calls(
                [
                    call(-1, "active_test"),
                    call(-1, "question_index"),
                    call(-1, "right_answers_number"),
                ]
            )


class TestTest:
    @patch("src.test.Question")
    def test__init__(self, mock_question: Mock) -> None:
        first_question = Question("", {}, "", None)
        second_question = Question("", {}, "", None)
        test = Test(
            command="/test_test",
            name="Проверочный тест",
            description="Описание теста.",
            questions=[first_question, second_question],
            result_explanation={
                "0": "zero",
                "3": "three",
                "1": "one",
                "2": "two",
            },
        )

        assert test.command == "/test_test"
        assert test.name == "Проверочный тест"
        assert test.description == "Описание теста."
        assert test.questions == [
            first_question,
            second_question,
        ]
        assert test.result_explanation == {
            0: "zero",
            1: "one",
            2: "two",
            3: "three",
        }

    @patch("src.test.Test.__init__", return_value=None)
    def test__eq__(self, mock__init__: Mock) -> None:
        first_test = Test("", "", None, [], None)
        first_test._command = "/a"

        second_test = Test("", "", None, [], None)
        second_test._command = "/a"

        assert first_test == second_test

    @patch("src.test.Test.__init__", return_value=None)
    def test__le__(self, mock__init__: Mock) -> None:
        first_test = Test("", "", None, [], None)
        first_test._command = "/b"

        second_test = Test("", "", None, [], None)
        second_test._command = "/b"

        assert first_test <= second_test

        first_test._command = "/a"
        assert first_test <= second_test

    @patch("src.test.Test.__init__", return_value=None)
    def test__lt__(self, mock__init__: Mock) -> None:
        first_test = Test("", "", None, [], None)
        first_test._command = "/a"

        second_test = Test("", "", None, [], None)
        second_test._command = "/b"

        assert first_test < second_test

    @patch("src.test.Test.__init__", return_value=None)
    def test__ge__(self, mock__init__: Mock) -> None:
        first_test = Test("", "", None, [], None)
        first_test._command = "/b"

        second_test = Test("", "", None, [], None)
        second_test._command = "/b"

        assert first_test >= second_test

        second_test._command = "/a"
        assert first_test >= second_test

    @patch("src.test.Test.__init__", return_value=None)
    def test__gt__(self, mock__init__: Mock) -> None:
        first_test = Test("", "", None, [], None)
        first_test._command = "/b"

        second_test = Test("", "", None, [], None)
        second_test._command = "/a"

        assert first_test > second_test


@patch("src.test.Question.check", new_callable=AsyncMock)
@patch("src.test.Question.__init__")
@patch("src.test.Test.__init__")
@patch("src.test.User.get")
@pytest.mark.asyncio
class TestCheck:
    @patch("src.test.Question.__call__", new_callable=AsyncMock)
    async def test_check_next_question(
        self,
        mock_question__call__: AsyncMock,
        mock_user_get: Mock,
        mock_test__init__: Mock,
        mock_question__init__: Mock,
        mock_question_check: AsyncMock,
    ) -> None:
        mock_user_get.return_value = 1
        mock_test__init__.return_value = None
        mock_question__init__.return_value = None

        test = Test("", "", None, [], None)
        test._questions = [
            Question("", {}, "", None),
            Question("", {}, "", None),
            Question("", {}, "", None),
        ]
        await test.check(-1, "Правильный ответ")

        mock_user_get.assert_called_once_with(-1, "question_index")
        test._questions[1].check.assert_awaited_once_with(-1, "Правильный ответ")  # type: ignore
        test._questions[2].__call__.assert_awaited_once_with(-1)  # type: ignore

    @patch("src.test.Test._finish", new_callable=AsyncMock)
    async def test_check_finish(
        self,
        mock_finish: AsyncMock,
        mock_user_get: Mock,
        mock_test__init__: Mock,
        mock_question__init__: Mock,
        mock_question_check: Mock,
    ) -> None:
        mock_user_get.return_value = 1
        mock_test__init__.return_value = None
        mock_question__init__.return_value = None

        test = Test("", "", None, [], None)
        test._questions = [Question("", {}, "", None), Question("", {}, "", None)]
        await test.check(-1, "Правильный ответ")

        mock_user_get.assert_called_once_with(-1, "question_index")
        test._questions[1].check.assert_awaited_once_with(-1, "Правильный ответ")  # type: ignore
        mock_finish.assert_awaited_once_with(-1)


@patch("src.test.Test.__init__", return_value=None)
@patch("src.test.Question.__init__", return_value=None)
@patch("src.test.Question.__call__", new_callable=AsyncMock)
@patch("src.test.User.set")
@patch("src.test.User.delete")
@patch("src.test.bot.send_message", new_callable=AsyncMock)
class TestStart:
    @pytest.mark.asyncio
    async def test_start(
        self,
        mock_send_message: AsyncMock,
        mock_user_delete: Mock,
        mock_user_set: Mock,
        mock_question__call__: AsyncMock,
        mock_question__init__: Mock,
        mock_test__init__: Mock,
    ) -> None:
        test = Test("", "", None, [], None)
        test._command = "/test_test"
        test._questions = [
            Question("", {}, "", None),
            Question("", {}, "", None),
            Question("", {}, "", None),
        ]
        await test.start(-1)

        mock_user_delete.assert_has_calls([call(-1, "checked")])
        mock_user_set.assert_has_calls(
            [
                call(-1, active_test="/test_test"),
                call(-1, question_index=0),
                call(-1, right_answers_number=0),
            ]
        )

        mock_calls = mock_send_message.mock_calls[0]
        assert mock_calls.args == (-1, "Тест начался!")
        assert isinstance(mock_calls.kwargs["reply_markup"], ReplyKeyboardRemove)
        test._questions[0].__call__.assert_awaited_once_with(-1)  # type: ignore


@patch("src.test.Test.__init__", return_value=None)
@pytest.mark.asyncio
class TestStop:
    @patch("src.test.Test._finish", new_callable=AsyncMock)
    async def test_stop(self, mock_finish: AsyncMock, test__init__: Mock) -> None:
        test = Test("", "", None, [], None)
        await test.stop(-1)

        mock_finish.assert_awaited_once_with(-1, is_stop=True)
