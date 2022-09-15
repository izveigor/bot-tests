"""Этот модуль содержит строителя тестов.

Классы:
    BuilderTest - открытый класс, строит тесты.
"""


import json
import os
from functools import partial
from multiprocessing import Manager, Pool, cpu_count
from typing import Any, Optional, Union
from zipfile import ZipFile

from telegram import Message

from src.test import Test
from src.user import User

from .bot import bot
from .constants import PATH_OF_DATA, REGEX_FILE
from .errors import BotFilesException
from .question import Question
from .singleton import Singleton
from .tree import CommandsTestTree, Node
from .validate import Validator


class BuilderTest(metaclass=Singleton):
    """Строитель тестов.

    Сохраняет, проверяет тесты.
    """

    def __init__(self) -> None:
        """При инициализации класса запускает обработку всех тестов из папки.

        Аргументы: -
        Возвращает: None
        """
        self._create_tests_from_files()

    async def create_test(
        self, from_user_id: int, file_content: dict[str, Any]
    ) -> None:
        directory = os.path.join(PATH_OF_DATA, str(from_user_id))
        if not os.path.exists(directory):
            os.mkdir(directory)  # pragma: no coverage

        files: list[str] = os.listdir(directory)
        number: int = self.get_directory_number(files, [])
        directory = os.path.join(directory, str(number))

        if not os.path.exists(directory):
            os.mkdir(directory)  # pragma: no coverage

        path = os.path.join(PATH_OF_DATA, str(from_user_id), str(number))

        with open(os.path.join(path, "test.json"), "w", encoding="utf-8") as f:
            json.dump(file_content, f)

        test = self._return_test(path, [])
        self._add_test(from_user_id, number, os.path.join(directory, test), [])

    async def create_test_by_json(
        self, message: Message, file_name: str, errors: list[Union[str, int]]
    ) -> None:
        """Создает тест, отправленным пользователем

        Аргументы:
            message - сообщение с документом, отправленным пользователем
            file_name - имя zip файла
            errors - список ошибок
        Возвращает: None
        """
        directory = os.path.join(PATH_OF_DATA, str(message.from_user.id))
        if not os.path.exists(directory):
            os.mkdir(directory)  # pragma: no coverage

        files: list[str] = os.listdir(directory)
        number: int = self.get_directory_number(files, errors)
        errors.append(number)
        directory = os.path.join(directory, str(number))

        file_info = await bot.get_file(file_id=message.document.file_id)
        if not os.path.exists(directory):
            os.mkdir(directory)  # pragma: no coverage
        path_to_file = os.path.join(directory, file_name)
        with open(path_to_file, "wb") as myzip:
            await file_info.download(out=myzip)

        with ZipFile(path_to_file, "r") as myzip:
            myzip.extractall(directory)

        os.remove(path_to_file)
        path = os.path.join(PATH_OF_DATA, str(message.from_user.id), str(number))

        test = self._return_test(path, errors)
        self._add_test(
            message.from_user.id, number, os.path.join(directory, test), errors
        )

    @staticmethod
    def _return_test(path: str, errors: list[Union[str, int]]) -> str:
        tests = []
        for file in os.listdir(path):
            if REGEX_FILE.match(file):
                tests.append(file)
            else:
                raise BotFilesException(
                    errors, "В директории присутствует файл с другим расширением."
                )

        if len(tests) == 0:
            raise BotFilesException(
                errors,
                'В директории отсутствует файл с расширением ".json".',
            )
        elif len(tests) > 1:
            raise BotFilesException(
                errors,
                'В директории более одного файла с расширением ".json".',
            )

        return tests[0]

    @staticmethod
    def get_directory_number(files: list[str], errors: list[Union[str, int]]) -> int:
        for number, directory_ in enumerate(files, start=1):
            if directory_ != str(number):
                break
            if number == 30:
                raise BotFilesException(
                    errors,
                    "У вас больше 30 тестов, вы больше не можете создавать тесты.",
                )
        else:
            if len(files) == 0:
                number = 1
            else:
                number += 1

        return number

    def _add_test(
        self, from_user_id: int, number: int, path: str, errors: list[Union[str, int]]
    ) -> None:
        files_content: list[tuple[int, int, dict[str, Any]]] = []
        initialized_tests: list[tuple[int, int, Test]] = []
        self._read_file(
            files_content,
            errors,
            from_user_id,
            number,
            path,
            is_raised=True,
        )
        self._validate(files_content[0][2], errors)
        self._initialize_test(
            initialized_tests, from_user_id, number, files_content[0][2]
        )
        User.add_test(from_user_id, number, initialized_tests[0][2].command)
        self._append_tests_to_tree(initialized_tests)

    def _find_tests(self) -> list[tuple[int, int, str]]:
        tests = []
        for root, _, files in os.walk(PATH_OF_DATA):
            for file in files:
                directory = root.replace(PATH_OF_DATA, "")[1:]
                from_user_id, number = list(map(int, directory.split("/")))
                tests.append((from_user_id, number, os.path.join(root, file)))
        return tests

    def _create_tests_from_files(self) -> None:
        files_content: Any
        initialized_tests: Any

        files_name = self._find_tests()
        if cpu_count() > 1:
            with Manager() as manager:
                with Pool(cpu_count() - 1) as pool:
                    files_content = manager.list()
                    initialized_tests = manager.list()

                    pool.starmap(
                        partial(self._read_file, files_content, []),
                        files_name,
                    )

                    pool.starmap(
                        partial(self._initialize_test, initialized_tests),
                        list(files_content),
                    )
                    initialized_tests = list(initialized_tests)
        else:
            files_content = list()
            initialized_tests = list()
            for (from_user_id, number, file_name) in files_name:
                self._read_file(files_content, [], from_user_id, number, file_name)

            for (from_user_id, number, file_content) in files_content:
                self._initialize_test(
                    initialized_tests, from_user_id, number, file_content
                )

        for (from_user_id, number, test) in initialized_tests:
            User.add_test(from_user_id, number, test.command)

        self._append_tests_to_tree(initialized_tests)

    def _read_file(
        self,
        files_content: Any,
        errors: list[Union[str, int]],
        from_user_id: int,
        number: int,
        file_name: str,
        is_raised: bool = False,
    ) -> None:
        with open(file_name) as file:
            file_json_content = file.read()
            try:
                file_content: dict[str, Any] = json.loads(file_json_content)
            except json.decoder.JSONDecodeError as error:
                if is_raised:
                    raise BotFilesException(
                        errors,
                        str(error),
                    )
                else:
                    raise error
            else:
                files_content.append((from_user_id, number, file_content))

    def _initialize_test(
        self,
        initialized_tests: Any,
        from_user_id: int,
        number: int,
        file_content: dict[str, Any],
    ) -> None:
        command: str = file_content["command"]
        name: str = file_content["name"]
        description: Optional[str] = file_content.get("description")
        questions: list[dict[str, Any]] = file_content["questions"]
        result_explanation: Optional[dict[str, Any]] = file_content.get(
            "result_explanation"
        )

        test_questions: list[Question] = []
        for question in questions:
            body = question["body"]
            widget = question.get("widget")
            answer = question["answer"]
            answer_explanation = question.get("answer_explanation")

            test_questions.append(Question(body, widget, answer, answer_explanation))

        initialized_tests.append(
            (
                from_user_id,
                number,
                Test(command, name, description, test_questions, result_explanation),
            )
        )

    def _append_tests_to_tree(
        self,
        tests: Any,
    ) -> None:
        for _, _, test in tests:
            CommandsTestTree().append(Node(key=test))

    def _validate(
        self, file_content: dict[str, Any], errors: list[Union[str, int]]
    ) -> None:
        command: Any = file_content.get("command")
        name: Any = file_content.get("name")
        description: Any = file_content.get("description")
        questions: Any = file_content.get("questions")
        result_explanation: Any = file_content.get("result_explanation")

        Validator(
            errors,
            command,
            name,
            description,
            questions,
            result_explanation,
        )
