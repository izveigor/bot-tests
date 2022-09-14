import json
from unittest.mock import AsyncMock, Mock, call, patch

import pytest
from fakeredis import FakeStrictRedis
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove

from src.constants import REDIS_SETTINGS
from src.graph import State
from src.user import User


@pytest.mark.asyncio
@patch("src.graph.bot.send_message")
class TestState:
    async def test_handle_if_length_next_is_one(self, mock_send_message: Mock):
        User.redis_ = FakeStrictRedis(**REDIS_SETTINGS)
        User.set(1, jsondata=json.dumps({"command": "/test_test"}))
        mock_validation = Mock()
        mock_handler = AsyncMock()
        state = State(
            0,
            [{"state": 1, "message": ""}],
            "questions.body.text",
            "",
            mock_validation,
            mock_handler,
        )
        await state.handle(1, "Текст")
        mock_handler.assert_awaited_once_with(
            {"command": "/test_test"},
            1,
            ["questions", "body", "text"],
            mock_validation,
            "Текст",
            [{"state": 1, "message": ""}],
        )

        mock_send_message.assert_not_called()

    async def test_handle_if_length_next_more_than_one(self, mock_send_message: Mock):
        User.redis_ = FakeStrictRedis(**REDIS_SETTINGS)
        User.set(1, jsondata=json.dumps({"command": "/test_test"}))
        User.set(1, state="0")
        mock_validation = Mock()
        mock_handler = AsyncMock()
        state = State(
            0,
            [{"state": 1, "message": "Да"}, {"state": 2, "message": "Нет"}],
            "questions.body.text",
            "",
            mock_validation,
            mock_handler,
        )
        await state.handle(1, "Да")
        mock_handler.assert_awaited_once_with(
            {"command": "/test_test"},
            1,
            ["questions", "body", "text"],
            mock_validation,
            "Да",
            [{"state": 1, "message": "Да"}, {"state": 2, "message": "Нет"}],
        )

        assert User.get(1, "state") == "1"
        _, kwargs = mock_send_message.call_args_list[0]

        assert kwargs["chat_id"] == 1
        assert kwargs["text"] == 'Вы нажали на кнопку "Да".'
        assert isinstance(kwargs["reply_markup"], ReplyKeyboardRemove)

    @patch("src.graph.User.delete")
    async def test_stop(self, mock_user_delete: Mock, mock_send_message: Mock):
        state = State(
            0,
            [{"state": 1, "message": ""}],
            "name",
            "",
            None,
            None,
        )
        await state.handle(1, "/stop")
        mock_user_delete.assert_has_calls(
            [
                call(1, "state"),
                call(1, "jsondata"),
            ]
        )
        mock_send_message.assert_called_once()

    @patch("src.graph.User.get")
    async def test_send_if_length_next_is_one(
        self, mock_user_get: Mock, mock_send_message: Mock
    ):
        mock_validate = Mock()
        mock_handler = AsyncMock()
        mock_user_get.return_value = 1
        message = "Введите имя теста:"
        state = State(
            0,
            [{"state": 1, "message": ""}],
            "name",
            message,
            mock_validate,
            mock_handler,
        )
        await state.send(1)
        mock_send_message.assert_called_once_with(1, message)

    @patch("src.graph.User.get")
    async def test_send_if_length_next_more_than_one(
        self, mock_user_get: Mock, mock_send_message: Mock
    ):
        mock_validate = Mock()
        mock_handler = AsyncMock()
        mock_user_get.return_value = 1
        message = "Хотите добавить описание теста?"
        state = State(
            0,
            [{"state": 3, "message": "Да"}, {"state": 5, "message": "Нет"}],
            "description",
            message,
            mock_validate,
            mock_handler,
        )
        await state.send(1)
        _, mock_kwargs = mock_send_message.call_args_list[0]

        assert mock_kwargs["chat_id"] == 1
        assert mock_kwargs["text"] == message
        assert isinstance(mock_kwargs["reply_markup"], ReplyKeyboardMarkup)

        assert mock_kwargs["reply_markup"]["keyboard"][0][0]["text"] == "Да"
        assert mock_kwargs["reply_markup"]["keyboard"][0][1]["text"] == "Нет"
