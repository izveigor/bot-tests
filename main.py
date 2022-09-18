import asyncio
import os
import shutil
from traceback import print_exception
from typing import Any, Union
from xml.dom import NoModificationAllowedErr

from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CallbackContext,
    CallbackQueryHandler,
    CommandHandler,
    MessageHandler,
    filters,
)

from src.builder import BuilderTest
from src.constants import PATH_OF_DATA, REGEX_COMMAND, REGEX_LIST
from src.errors import BotException, BotFilesException, BotParseException
from src.graph import STATES
from src.log import logger
from src.test import Test
from src.tree import CommandsTestTree, Node
from src.user import User


async def handle(state: str, update: Update, context: CallbackContext) -> None:
    int_state = int(state)
    await STATES[int_state].handle(update.effective_user.id, update.message.text)
    await STATES[int(User.get(update.effective_user.id, "state"))].send(
        update.effective_user.id
    )


async def create(update: Update, context: CallbackContext) -> None:
    path = os.path.join(PATH_OF_DATA, str(update.effective_user.id))
    if os.path.exists(path):
        BuilderTest().get_directory_number(os.listdir(path), [])
    try:
        state = User.get(update.effective_user.id, "state")
    except ValueError:
        User.set(update.effective_user.id, state="0")
        await context.bot.send_message(
            update.effective_user.id,
            text="Вы начали создание нового теста. Для того чтобы полностью создать тест, следуйте инструкциям снизу. Если вы перезахотели создавать тест, то пропишите команду /stop.",
        )
        await STATES[0].send(update.effective_user.id)
    else:
        await context.bot.send_message(
            update.effective_user.id,
            text="Вы не закончили процесс создания теста. Если вы хотите завершить его, то напишите команду /stop. Если вы хотите продолжить, то отвечайте на следующие инструкции:",
        )
        await STATES[int(state)].send(update.effective_user.id)


def allow(function: Any) -> Any:
    async def wrapper(update: Update, context: CallbackContext) -> Any:
        try:
            state = User.get(update.effective_user.id, "state")
        except ValueError:
            return await function(update, context)
        else:
            return await handle(state, update, context)

    return wrapper


@allow
async def start(update: Update, context: CallbackContext) -> None:
    await context.bot.send_message(
        update.effective_user.id,
        text=f"Приветствую тебя, {update.effective_user.first_name} {update.effective_user.last_name}. Если хочешь узнать больше информации про этого бота, пропиши /help.",
    )


@allow
async def help(update: Update, context: CallbackContext) -> None:
    await context.bot.send_message(
        update.effective_user.id,
        '*Описание*:\nБот создан для создания и решения разнообразных тестов. Тесты создаются на основе json-файла или последовательно с помощью команды /create.\n\n Вот список моих команд в алфавитном порядке 👇:\n/about - показывает информацию о боте\n/create - последовательное создание теста\n/delete \\[command] - удаляет тест. \n/help - показывает все возможные команды бота.\n/list \\[start-end] - показывает список тестов от start до end в алфавитном порядке (лимит - 50 тестов).\n/my\\_tests - показывает список тестов, которые создал пользователь.\n/start - приветствует пользователя и советует использовать команду /help.\n/start\\_test - начинает решение теста (работает только после команды "/test\\_{characters}")\n/stop - заканчивает тест и показывает результат пользователя (работает только после команды "/start\\_test").\n/test\\_{characters} - показывает описание теста, после слова "/test\\_" допускается использование прописных и строчных латинских букв, десятичных цифр и знака "\\_".\n\nЖелаю удачи в создании и в решении тестов!',
        parse_mode="Markdown",
    )


@allow
async def about(update: Update, context: CallbackContext) -> None:
    await context.bot.send_message(
        update.effective_user.id,
        "О боте:\nGithub: https://github.com/izveigor/bot-tests\nАвтор: Igor Izvekov\nEmail: izveigor@gmail.com\nLicense: MIT",
    )


@allow
async def my_tests(update: Update, context: CallbackContext) -> None:
    tests = User.get_tests(update.effective_user.id)
    if not tests or len(tests) == 0:
        await context.bot.send_message(
            update.effective_user.id, "Вы не создали ни одного теста."
        )
    else:
        await context.bot.send_message(
            update.effective_user.id,
            f"Ваши тесты ({len(tests)}/30):\n"
            + "\n".join(
                [str(number + 1) + " " + tests[number] for number in range(len(tests))]
            ),
        )


@allow
async def delete(update: Update, context: CallbackContext) -> None:
    _, test = update.message.text.split()
    if not REGEX_COMMAND.match(test):
        await context.bot.send_message(
            update.effective_user.id,
            'Команда не подходит под заданный шаблон. После слова /delete должен стоять пробел и слово, со следующими правилами: в начале должно стоять слово "test_". Далее к нему приписываются все буквы латинского алфавита (прописные и/или строчные) и/или десятичные цифры и/или _. Максимальная длина команды с учетом начального слова не должна превышать 40.',
        )
    else:
        if test in User.get_tests(update.effective_user.id):
            number = None
            for hset in User.get_tests_with_numbers(update.effective_user.id):
                if list(hset.values())[0] == test:
                    number = list(hset.keys())[0]
                    break
            found = CommandsTestTree().search(Node(Test(test, "", None, [], None)))
            if found:
                CommandsTestTree().delete(found)

            User.delete_test(update.effective_user.id, test)
            shutil.rmtree(
                os.path.join(PATH_OF_DATA, str(update.effective_user.id), str(number))
            )
            await context.bot.send_message(
                update.effective_user.id,
                f'Тест с командой "{test}" был успешно удален.',
            )
        else:
            await context.bot.send_message(
                update.effective_user.id, "Вы не являетесь владельцом этого теста."
            )


@allow
async def test(update: Update, context: CallbackContext) -> None:
    try:
        active_test = User.get(update.effective_user.id, "active_test")
    except ValueError:
        active_test = None

    if active_test is not None:
        await context.bot.send_message(
            update.effective_user.id,
            f'Вы не можете посмотреть другой тест, так как вы не закончили тест "{active_test}".',
        )
    else:
        if not REGEX_COMMAND.match(update.message.text):
            await context.bot.send_message(
                update.effective_user.id,
                'Команда не подходит под заданный шаблон. В начале должно стоять слово "test_". Далее к нему приписываются все буквы латинского алфавита (прописные и/или строчные) и/или десятичные цифры и/или _. Максимальная длина команды с учетом начального слова не должна превышать 40.',
            )
        else:
            test = CommandsTestTree().search(
                Node(Test(update.message.text, "", None, [], None))
            )
            if test is None:
                await context.bot.send_message(
                    update.effective_user.id,
                    f"Тест с командой {update.message.text} отсутствует. Убедитесь, что вы правильно набрали команду. Посмотреть список тестов можно по команде /list [range].",
                )
            else:
                await test.key.see(update.effective_user.id)


@allow
async def start_test(update: Update, context: CallbackContext) -> None:
    try:
        test_command = User.get(update.effective_user.id, "checked")
    except ValueError:
        test_command = None

    if test_command is None:
        await context.bot.send_message(
            update.effective_user.id,
            "Вы не можете запустить тест, так как вы не посмотрели ни одного теста.",
        )
    else:
        test = CommandsTestTree().search(Node(Test(test_command, "", None, [], None)))
        if test:
            await test.key.start(update.effective_user.id)


@allow
async def stop(update: Update, context: CallbackContext) -> None:
    try:
        test_command = User.get(update.effective_user.id, "active_test")
    except ValueError:
        test_command = None

    if test_command is None:
        await context.bot.send_message(
            update.effective_user.id,
            "Вы не можете закончить тест, так как вы не начали ни одного теста.",
        )
    else:
        test = CommandsTestTree().search(Node(Test(test_command, "", None, [], None)))
        if test:
            await test.key.stop(update.effective_user.id)


@allow
async def list_(update: Update, context: CallbackContext) -> None:
    if not REGEX_LIST.match(update.message.text):
        await context.bot.send_message(
            update.effective_user.id,
            'Команда не подходит под заданный шаблон. После слова "/list" должен стоять пробел, положительная десятичная цифра, знак "-" и еще одна положительная десятичная цифра.',
        )
    else:
        _, range_ = update.message.text.split()
        start, end = list(map(int, range_.split("-")))
        if start > end:
            await context.bot.send_message(
                update.effective_user.id,
                "Начальная десятичная цифра должна быть меньше или равной конечной десятичной цифры.",
            )
        elif end - start + 1 > 50:
            await context.bot.send_message(
                update.effective_user.id,
                "Количество элементов в промежутке не должно превышать 50.",
            )
        else:
            list_tests = "\n".join(
                [test for test in CommandsTestTree().sort()[start : end + 1]]
            )
            await context.bot.send_message(
                update.effective_user.id,
                list_tests if list_tests else "Тесты отсутствуют.",
            )


@allow
async def other_message(update: Update, context: CallbackContext) -> None:
    try:
        active_test = User.get(update.effective_user.id, "active_test")
    except ValueError:
        active_test = None

    if active_test is None:
        await context.bot.send_message(
            update.effective_user.id,
            "Такой команды нет, если хочешь увидеть список всех возможных команд, набери /help.",
        )
    else:
        test = CommandsTestTree().search(Node(Test(active_test, "", None, [], None)))
        if test:
            await test.key.check(update.effective_user.id, update.message.text)


async def button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    markup = query["message"]["reply_markup"]
    if query.data == "1":
        if "✅" not in markup.inline_keyboard[0][0].text:
            markup.inline_keyboard[0][0].text += "✅"
        else:
            markup.inline_keyboard[0][0].text = markup.inline_keyboard[0][0].text[:-1]
        await query.edit_message_reply_markup(
            reply_markup=markup,
        )
    elif query.data == "2":
        if "✅" not in markup.inline_keyboard[0][1].text:
            markup.inline_keyboard[0][1].text += "✅"
        else:
            markup.inline_keyboard[0][1].text = markup.inline_keyboard[0][1].text[:-1]
        await query.edit_message_reply_markup(
            reply_markup=markup,
        )
    elif query.data == "3":
        if "✅" not in markup.inline_keyboard[1][0].text:
            markup.inline_keyboard[1][0].text += "✅"
        else:
            markup.inline_keyboard[1][0].text = markup.inline_keyboard[1][0].text[:-1]
        await query.edit_message_reply_markup(
            reply_markup=markup,
        )
    elif query.data == "4":
        if "✅" not in markup.inline_keyboard[1][1].text:
            markup.inline_keyboard[1][1].text += "✅"
        else:
            markup.inline_keyboard[1][1].text = markup.inline_keyboard[1][1].text[:-1]
        await query.edit_message_reply_markup(
            reply_markup=markup,
        )
    elif query.data == "Ответить":
        active_test = User.get(query["from"]["id"], "active_test")

        answer = []
        for i in range(len(markup.inline_keyboard)):
            for j in range(len(markup.inline_keyboard[i])):
                if "✅" in markup.inline_keyboard[i][j].text:
                    answer.append(i * 2 + j + 1)

        test = CommandsTestTree().search(Node(Test(active_test, "", None, [], None)))
        if test:
            await test.key.check(query["from"]["id"], answer)


async def get_document_messages(update: Update, context: CallbackContext) -> None:
    file_name = update.message.document.file_name
    if update.message.caption == "/create" and ".zip" in file_name:
        errors: list[Union[str, int]] = []
        try:
            await asyncio.gather(
                BuilderTest().create_test_by_json(update.message, file_name, errors)
            )
        except BotParseException:
            shutil.rmtree(
                os.path.join(
                    PATH_OF_DATA, str(update.message.from_user.id), str(errors[0])
                )
            )
            await context.bot.send_message(
                update.message.from_user.id,
                "Произошла следующая ошибка в тестовом файле: " + f'"{errors[1]}".',
            )
        except BotFilesException:
            if isinstance(errors[0], int):
                shutil.rmtree(
                    os.path.join(
                        PATH_OF_DATA, str(update.message.from_user.id), str(errors[0])
                    )
                )
                error_message = errors[1]
            else:
                error_message = errors[0]

            await context.bot.send_message(
                update.message.from_user.id,
                "Произошла следующая ошибка с обработкой файлов: "
                + f'"{error_message}".',
            )
        except Exception as error:
            logger.error(error)
        else:
            await context.bot.send_message(
                update.message.from_user.id,
                "Тест был успешно создан.",
            )
    else:
        await context.bot.send_message(
            update.message.from_user.id,
            'Файл не был принят. Если вы хотите создать тест, отправьте zip файл с caption "/create".',
        )


def start_bot() -> None:
    application = ApplicationBuilder().token(os.environ.get("TELEGRAM_TOKEN")).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help))
    application.add_handler(CommandHandler("about", about))
    application.add_handler(CommandHandler("my_tests", my_tests))
    application.add_handler(CommandHandler("start_test", start_test))
    application.add_handler(CommandHandler("stop", stop))
    application.add_handler(CommandHandler("delete", delete))
    application.add_handler(CommandHandler("create", create))

    application.add_handler(CallbackQueryHandler(button))
    application.add_handler(MessageHandler(filters.Regex(r"^/list+"), list_))
    application.add_handler(MessageHandler(filters.Regex(r"^/test_+"), test))
    application.add_handler(MessageHandler(filters.TEXT, other_message))
    application.add_handler(MessageHandler(filters.Document.ALL, get_document_messages))

    application.run_polling()


def main() -> None:
    try:
        start_bot()
    except Exception as error:
        if not issubclass(type(error), BotException) and not issubclass(
            type(error), TimeoutError
        ):
            print_exception(error)
            logger.error(error)
        else:
            main()


if __name__ == "__main__":
    BuilderTest()
    if not os.path.exists(PATH_OF_DATA):
        os.mkdir(PATH_OF_DATA)
    main()
