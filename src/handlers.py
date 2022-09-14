import json
from importlib.metadata import packages_distributions
from tempfile import TemporaryFile
from typing import Any, Callable, Optional

from telegram import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove

from . import validate
from .bot import bot
from .builder import BuilderTest
from .errors import BotParseException
from .user import User

"""async def _validate(*args):"""


async def command_handler(
    file_content, from_user_id: int, fields, validation, message, next_
):
    errors = []
    try:
        validation(message, errors)
    except BotParseException:
        await bot.send_message(
            from_user_id,
            errors[0],
        )
    else:
        User.set(from_user_id, jsondata=json.dumps({fields[0]: message}))
        User.set(from_user_id, state=next_[0]["state"])


async def name_handler(file_content, from_user_id, fields, validation, message, next_):
    errors = []
    try:
        validation(message, errors)
    except BotParseException:
        await bot.send_message(
            from_user_id,
            errors[0],
        )
    else:
        file_content[fields[0]] = message
        User.set(from_user_id, jsondata=json.dumps(file_content))
        User.set(from_user_id, state=next_[0]["state"])


async def description_handler(
    file_content, from_user_id, fields, validation, message, next_
):
    errors = []
    if file_content.get(fields[0]) is None:
        file_content[fields[0]] = {}
    file_content[fields[0]][fields[1]] = message
    try:
        validation(file_content[fields[0]], errors)
    except BotParseException:
        await bot.send_message(
            from_user_id,
            errors[0],
        )
    else:
        User.set(from_user_id, jsondata=json.dumps(file_content))
        User.set(from_user_id, state=next_[0]["state"])


async def body_handler(file_content, from_user_id, fields, validation, message, next_):
    errors = []
    if fields[1] == "body" and fields[2] == "text":
        if file_content.get(fields[0]) is None:
            file_content[fields[0]] = [{}]
        else:
            file_content[fields[0]].append({})

    if file_content[fields[0]][len(file_content[fields[0]]) - 1].get(fields[1]) is None:
        file_content[fields[0]][len(file_content[fields[0]]) - 1][fields[1]] = {}
    file_content[fields[0]][len(file_content[fields[0]]) - 1][fields[1]][
        fields[2]
    ] = message
    try:
        validation(
            file_content[fields[0]][len(file_content[fields[0]]) - 1][fields[1]], errors
        )
    except BotParseException:
        await bot.send_message(
            from_user_id,
            errors[0],
        )
    else:
        User.set(from_user_id, jsondata=json.dumps(file_content))
        User.set(from_user_id, state=next_[0]["state"])


async def widget_handler(
    file_content, from_user_id, fields, validation, message, next_
):
    body = file_content[fields[0]][len(file_content[fields[0]]) - 1][fields[1]].get(
        fields[2]
    )
    if not (body and len(body) == 4):
        errors = []
        if (
            file_content[fields[0]][len(file_content[fields[0]]) - 1][fields[1]].get(
                fields[2]
            )
            is None
        ):
            file_content[fields[0]][len(file_content[fields[0]]) - 1][fields[1]][
                fields[2]
            ] = []
        file_content[fields[0]][len(file_content[fields[0]]) - 1][fields[1]][
            fields[2]
        ].append(message)
        try:
            validation(
                file_content[fields[0]][len(file_content[fields[0]]) - 1][fields[1]][
                    fields[2]
                ],
                file_content[fields[0]][len(file_content[fields[0]]) - 1][fields[1]][
                    "type"
                ],
                errors,
            )
        except BotParseException:
            await bot.send_message(
                from_user_id,
                errors[0],
            )
        else:
            User.set(from_user_id, jsondata=json.dumps(file_content))
            User.set(from_user_id, state=next_[0]["state"])
    else:
        await bot.send_message(
            from_user_id, "Вы не можете создать больше кнопок, вы достигли лимита!"
        )
        User.set(from_user_id, state="10")


async def type_handler(file_content, from_user_id, fields, validation, message, next_):
    errors = []
    if file_content[fields[0]][len(file_content[fields[0]]) - 1].get(fields[1]) is None:
        file_content[fields[0]][len(file_content[fields[0]]) - 1][fields[1]] = {}
    file_content[fields[0]][len(file_content[fields[0]]) - 1][fields[1]][
        fields[2]
    ] = message
    try:
        validation(
            file_content[fields[0]][len(file_content[fields[0]]) - 1][fields[1]][
                fields[2]
            ],
            errors,
        )
    except BotParseException:
        await bot.send_message(
            from_user_id,
            errors[0],
        )
    else:
        User.set(from_user_id, jsondata=json.dumps(file_content))
        User.set(from_user_id, state=next_[0]["state"])


async def answer_handler(
    file_content, from_user_id, fields, validation, message, next_
):
    errors = []
    file_content[fields[0]][len(file_content[fields[0]]) - 1][fields[1]] = message
    widget = file_content[fields[0]][len(file_content[fields[0]]) - 1]["widget"]
    if widget["type"] == "button":
        try:
            answer = int(message)
        except ValueError:
            answer = ""
    elif widget["type"] == "checkbox":
        try:
            answer = list(map(int, message.split("-")))
        except ValueError:
            answer = ""
    else:
        answer = message

    try:
        validation(answer, widget, errors)
    except BotParseException:
        await bot.send_message(
            from_user_id,
            errors[0],
        )
    else:
        User.set(from_user_id, jsondata=json.dumps(file_content))
        User.set(from_user_id, state=next_[0]["state"])


async def result_explanation_handler(
    file_content, from_user_id, fields, validation, message, next_
):
    errors = []
    if file_content.get(fields[0]) is None:
        file_content[fields[0]] = {}
    file_content[fields[0]][message] = {}
    try:
        validation(file_content[fields[0]], len(file_content["questions"]), errors)
    except BotParseException:
        await bot.send_message(
            from_user_id,
            errors[0],
        )
    else:
        User.set(from_user_id, jsondata=json.dumps(file_content))
        User.set(from_user_id, state=next_[0]["state"])


async def result_explanation_text_handler(
    file_content, from_user_id, fields, validation, message, next_
):
    errors = []
    last_key = list(file_content[fields[0]].keys())[len(file_content[fields[0]]) - 1]
    file_content[fields[0]][last_key][fields[1]] = message
    try:
        validation(file_content[fields[0]], len(file_content["questions"]), errors)
    except BotParseException:
        await bot.send_message(
            from_user_id,
            errors[0],
        )
    else:
        User.set(from_user_id, jsondata=json.dumps(file_content))
        User.set(from_user_id, state=next_[0]["state"])
