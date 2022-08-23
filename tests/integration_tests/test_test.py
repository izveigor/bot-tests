from unittest.mock import Mock, call, patch

import pytest
from fakeredis import FakeStrictRedis
from telegram import InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove

from src.constants import REDIS_SETTINGS
from src.question import Question
from src.test import Test
from src.user import User


@patch("src.test.bot.send_photo")
@patch("src.test.bot.send_message")
@pytest.mark.asyncio
async def test_Test(mock_send_message: Mock, mock_send_photo: Mock) -> None:
    User.redis_ = FakeStrictRedis(**REDIS_SETTINGS)
    user_id = 1

    test = Test(
        command="/test_test",
        name="Name",
        description=None,
        questions=[
            Question(
                body="Вопрос 1",
                widget={
                    "type": "input",
                },
                answer="Ответ 1",
                answer_explanation=None,
            ),
            Question(
                body={
                    "text": "Вопрос 2",
                },
                widget={
                    "type": "button",
                    "body": [
                        "Yes",
                        "No",
                    ],
                },
                answer=1,
                answer_explanation='Надо было нажать "Yes".',
            ),
            Question(
                body={
                    "text": "Вопрос 3",
                    "url": "photo.png",
                },
                widget={
                    "type": "checkbox",
                    "body": [
                        "1",
                        "2",
                        "3",
                        "4",
                    ],
                },
                answer=[1, 3],
                answer_explanation="Надо было выбрать 1 и 3.",
            ),
        ],
        result_explanation={
            "1": "Хорошо",
            "0": "Плохо",
        },
    )

    assert test.command == "/test_test"
    assert test.name == "Name"
    assert test.description == "Описание отсутствует."
    assert len(test.questions) == 3
    for question in test.questions:
        assert isinstance(question, Question)
    assert test.result_explanation == {
        0: "Плохо",
        1: "Хорошо",
    }

    await test.see(user_id)
    assert User.get(user_id, "checked") == test.command
    assert mock_send_message.mock_calls[0].args == (
        user_id,
        "Название: Name\nОписание:\nОписание отсутствует.",
    )
    print(mock_send_message.mock_calls[0])
    assert isinstance(
        mock_send_message.mock_calls[0].kwargs["reply_markup"], ReplyKeyboardMarkup
    )

    await test.start(user_id)
    with pytest.raises(ValueError):
        User.get(user_id, "checked")

    assert User.get(user_id, "active_test") == test.command
    assert User.get(user_id, "question_index") == "0"
    assert User.get(user_id, "right_answers_number") == "0"

    assert mock_send_message.mock_calls[1].args == (1, "Тест начался!")
    assert isinstance(
        mock_send_message.mock_calls[1].kwargs["reply_markup"], ReplyKeyboardRemove
    )
    mock_send_message.mock_calls[2] == call(user_id, "Вопрос 1", reply_markup=None)

    await test.check(user_id, "Ответ 1")
    assert User.get(user_id, "question_index") == "1"
    assert User.get(user_id, "right_answers_number") == "1"

    mock_send_message.mock_calls[3] == call(
        user_id,
        'Правильно ✅\nВаш ответ: "Ответ 1"\nПравильный ответ: "Ответ 1"\nОбъяснение ответа:\nОбъяснение ответа отсутствует.',
    )

    mock_args, mock_kwargs = mock_send_message.call_args_list[4]
    assert mock_kwargs["chat_id"] == 1
    assert mock_kwargs["text"] == "Вопрос 2"
    assert isinstance(mock_kwargs["reply_markup"], ReplyKeyboardMarkup)

    assert mock_kwargs["reply_markup"].keyboard[0][0].text == "Yes"
    assert mock_kwargs["reply_markup"].keyboard[0][1].text == "No"

    await test.check(user_id, "No")
    assert User.get(user_id, "question_index") == "2"
    assert User.get(user_id, "right_answers_number") == "1"

    mock_send_message.mock_calls[5] == call(
        user_id,
        'Неправильно ❌\nВаш ответ: "No"\nПравильный ответ: "Yes"\nОбъяснение ответа:\nНадо было нажать "Yes".',
    )

    mock_args, mock_kwargs = mock_send_photo.call_args_list[0]
    assert mock_kwargs["chat_id"] == 1
    assert mock_kwargs["photo"] == "photo.png"
    assert mock_kwargs["caption"] == "Вопрос 3"
    assert isinstance(mock_kwargs["reply_markup"], InlineKeyboardMarkup)

    for testing_row, row in zip(
        [
            [{"text": "1"}, {"text": "2"}],
            [{"text": "3"}, {"text": "4"}],
            [{"text": "Ответить"}],
        ],
        mock_kwargs["reply_markup"].inline_keyboard,
    ):
        for inline_button, testing_data in zip(row, testing_row):
            assert inline_button.text == testing_data["text"]

    await test.stop(user_id)

    with pytest.raises(ValueError):
        User.get(user_id, "active_test") is None
    with pytest.raises(ValueError):
        User.get(user_id, "question_index") is None
    with pytest.raises(ValueError):
        User.get(user_id, "right_answers_number") is None

    mock_send_message.mock_calls[5].kwargs["chat_id"] == 1
    mock_send_message.mock_calls[5].kwargs["text"] == "Хорошо"
