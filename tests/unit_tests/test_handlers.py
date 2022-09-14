import json
from unittest.mock import Mock, patch

import pytest
from fakeredis import FakeStrictRedis

from src import handlers
from src.constants import REDIS_SETTINGS
from src.user import User


@pytest.mark.asyncio
@patch("src.handlers.bot.send_message")
class TestHandlers:
    @pytest.mark.parametrize(
        (
            "handler",
            "file_content",
            "fields",
            "message",
            "result_fields",
            "result_message",
        ),
        [
            (
                handlers.command_handler,
                None,
                ["command"],
                "/test_test",
                ["command"],
                "/test_test",
            ),
            (
                handlers.name_handler,
                {"command": "/test_test"},
                ["name"],
                "Имя",
                ["name"],
                "Имя",
            ),
            (
                handlers.description_handler,
                {"command": "/test_test", "name": "Имя"},
                ["description", "text"],
                "Текст",
                ["description", "text"],
                "Текст",
            ),
            (
                handlers.body_handler,
                {"command": "/test_test"},
                ["questions", "body", "text"],
                "Как звали Пушкина?",
                ["questions"],
                [{"body": {"text": "Как звали Пушкина?"}}],
            ),
            (
                handlers.widget_handler,
                {
                    "questions": [
                        {
                            "body": {"text": "Как звали Пушкина?"},
                            "widget": {"type": "button"},
                        }
                    ]
                },
                ["questions", "widget", "body"],
                "Первый пункт",
                ["questions", 0, "widget"],
                {"type": "button", "body": ["Первый пункт"]},
            ),
            (
                handlers.type_handler,
                {"questions": [{"body": {"text": "Как звали Пушкина?"}}]},
                ["questions", "widget", "type"],
                "input",
                ["questions", 0, "widget"],
                {"type": "input"},
            ),
            (
                handlers.answer_handler,
                {
                    "questions": [
                        {
                            "body": {"text": "Как звали Пушкина?"},
                            "widget": {"type": "input"},
                        }
                    ]
                },
                ["questions", "answer"],
                "Александр",
                ["questions", 0, "answer"],
                "Александр",
            ),
            (
                handlers.result_explanation_handler,
                {"questions": []},
                ["result_explanation"],
                "0",
                ["result_explanation"],
                {"0": {}},
            ),
            (
                handlers.result_explanation_text_handler,
                {"questions": [], "result_explanation": {"0": {}}},
                ["result_explanation", "text"],
                "Объяснение",
                ["result_explanation", "0"],
                {"text": "Объяснение"},
            ),
        ],
    )
    async def test_handlers(
        self,
        mock_send_message: Mock,
        handler,
        file_content,
        fields,
        message,
        result_fields,
        result_message,
    ):
        User.redis_ = FakeStrictRedis(**REDIS_SETTINGS)
        validation = Mock()
        await handler(file_content, 1, fields, validation, message, [{"state": 1}])
        mock_send_message.assert_not_called()
        value = json.loads(User.get(1, "jsondata"))
        for argument in result_fields:
            value = value[argument]
        assert value == result_message
        assert User.get(1, "state") == "1"
