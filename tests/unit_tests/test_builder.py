import re
from datetime import datetime
from json import JSONDecodeError
from typing import Any, Callable, Iterable, Union
from unittest.mock import AsyncMock, Mock, call, patch

import pytest
import telegram
from pytest import Config

from src.builder import BuilderTest
from src.constants import PATH_OF_DATA
from src.errors import BotFilesException
from src.question import Question
from src.test import Test
from src.tree import ColorTree, Node


class TestBuilder:
    @patch("src.builder.BuilderTest._create_tests_from_files")
    def test__init__(
        self, mock_create_tests_from_files: Mock, patch_singleton: Config
    ) -> None:
        BuilderTest()
        mock_create_tests_from_files.assert_called_once()


@patch("src.builder.bot.get_file", new_callable=AsyncMock)
@patch("src.builder.BuilderTest._add_test")
@patch("src.builder.BuilderTest._return_test")
@patch("src.builder.BuilderTest._get_directory_number")
@patch("src.builder.os.remove")
@patch("src.builder.ZipFile")
@patch("src.builder.open")
@patch("src.builder.os.listdir")
@patch("src.builder.os.path.exists")
@patch("src.builder.BuilderTest.__init__", return_value=None)
@pytest.mark.asyncio
class TestCreateTest:
    @staticmethod
    def create_document(caption: str) -> telegram.Message:
        chat = telegram.User(id=-1, is_bot=False, first_name="Иван", last_name="Иванов")
        message = telegram.Message(
            message_id=-1, from_user=chat, chat=chat, text="text", date=datetime.now()
        )
        message.caption = caption
        message.document = telegram.Document(
            file_id=-1, file_unique_id=1, file_name="test.zip"
        )
        return message

    async def test_create_test(
        self,
        mock__init__: Mock,
        mock_path_exists: Mock,
        mock_listdir: Mock,
        mock_open: Mock,
        mock_ZipFile: Mock,
        mock_remove: Mock,
        mock_get_directory_number: Mock,
        mock_return_test: Mock,
        mock_add_test: Mock,
        mock_get_file: Mock,
    ) -> None:
        errors: list[Union[str, int]] = []
        message = self.create_document("/create")
        mock_listdir.return_value = [str(i) for i in range(1, 6)]
        mock_get_directory_number.return_value = 1
        mock_return_test.return_value = "test.json"
        file_mock = AsyncMock()
        file_mock.download_file.return_value = "data_from_download_file"
        mock_get_file.return_value = file_mock
        await BuilderTest().create_test(message, "file.zip", errors)

        path_to_file = PATH_OF_DATA + "/-1/1/file.zip"
        mock_get_directory_number.assert_called_once_with(
            [str(i) for i in range(1, 6)], errors
        )
        mock_get_file.assert_called_once_with(
            file_id="-1",
        )

        mock_path_exists.assert_has_calls(
            [
                call(PATH_OF_DATA + "/-1"),
                call().__bool__(),
                call(PATH_OF_DATA + "/-1/1"),
                call().__bool__(),
            ]
        )

        assert errors[0] == 1

        mock_open.assert_called_once_with(path_to_file, "wb")

        mock_ZipFile.assert_called_once_with(path_to_file, "r")
        mock_ZipFile().__enter__().extractall.assert_called_once_with(
            PATH_OF_DATA + "/-1/1"
        )

        mock_remove.assert_called_once_with(path_to_file)

        mock_return_test.assert_called_once_with(PATH_OF_DATA + "/-1/1", errors)

        mock_add_test.assert_called_once_with(
            -1,
            1,
            PATH_OF_DATA + "/-1/1/test.json",
            errors,
        )


@patch("src.builder.os.listdir")
@patch("src.builder.BuilderTest.__init__", return_value=None)
class TestReturnTest:
    def test_right(self, mock__init__: Mock, mock_listdir: Mock) -> None:
        errors: list[Union[str, int]] = []
        mock_listdir.return_value = ["test.json"]
        test = BuilderTest()._return_test("path", errors)
        assert test == "test.json"

    @pytest.mark.parametrize(
        ("return_listdir", "error"),
        [
            (
                ["test.json", "image.png"],
                "В директории присутствует файл с другим расширением.",
            ),
            (["image.png"], "В директории присутствует файл с другим расширением."),
            (
                [],
                'В директории отсутствует файл с расширением ".json".',
            ),
            (
                ["test.json", "another_test.json"],
                'В директории более одного файла с расширением ".json".',
            ),
        ],
    )
    def test_error(
        self,
        mock__init__: Mock,
        mock_listdir: Mock,
        return_listdir: list[str],
        error: str,
    ) -> None:
        errors: list[Union[str, int]] = []
        mock_listdir.return_value = return_listdir
        with pytest.raises(
            BotFilesException,
        ):
            BuilderTest()._return_test("path", errors)
        re.match(error, str(errors[0]))


@patch("src.builder.BuilderTest.__init__", return_value=None)
class TestGetDirectoryNumber:
    @pytest.mark.parametrize(
        ("files", "result_number"),
        [
            (["1", "2", "3", "4", "5"], 6),
            (["1", "2", "4", "5"], 3),
            (["2", "3"], 1),
            ([], 1),
        ],
    )
    def test_right(
        self, mock__init__: Mock, files: list[str], result_number: int
    ) -> None:
        number = BuilderTest()._get_directory_number(files, [])
        assert number == result_number

    def test_number_more_than_30(self, mock__init__: Mock) -> None:
        errors: list[Union[str, int]] = []
        with pytest.raises(
            BotFilesException,
        ):
            BuilderTest()._get_directory_number([str(i) for i in range(1, 31)], errors)
        re.match(
            "У вас больше 30 тестов, вы больше не можете создавать тесты.",
            str(errors[0]),
        )


@patch("src.builder.Test.__init__", return_value=None)
@patch("src.builder.BuilderTest._append_tests_to_tree")
@patch("src.builder.User.add_test")
@patch("src.builder.BuilderTest._initialize_test")
@patch("src.builder.BuilderTest._validate")
@patch("src.builder.BuilderTest._read_file")
@patch("src.builder.BuilderTest.__init__", return_value=None)
class TestAddTest:
    def test_add_test(
        self,
        mock__init__: Mock,
        mock_read_file: Mock,
        mock_validate: Mock,
        mock_initialize_test: Mock,
        mock_add_test: Mock,
        mock_append_tests_to_tree: Mock,
        mock_test__init__: Mock,
    ) -> None:
        errors: list[Union[str, int]] = []

        def _mock_read_file(
            content: list[tuple[int, int, str]],
            errors: list[Union[str, int]],
            from_user_id: int,
            number: int,
            path: str,
            is_raised: bool,
        ) -> None:
            content.append((from_user_id, number, '{"command": "/test_test"}'))
            return

        class_ = Test("", "", None, [], None)
        class_._command = "0"

        def _mock_initialize_test(
            initialized_tests: list[tuple[int, int, Test]],
            from_user_id: int,
            number: int,
            file_content: dict[str, Any],
        ) -> None:
            initialized_tests.append((from_user_id, number, class_))
            return

        mock_read_file.side_effect = _mock_read_file
        mock_initialize_test.side_effect = _mock_initialize_test

        BuilderTest()._add_test(1, 2, "path", errors)

        mock_validate.assert_called_once_with('{"command": "/test_test"}', errors)
        mock_add_test.assert_called_once_with(1, 2, "0")
        mock_calls = mock_append_tests_to_tree.mock_calls[0].args[0][0]

        assert mock_calls[0] == 1
        assert mock_calls[1] == 2
        assert mock_calls[2] is class_


class TestFindTests:
    @patch("src.builder.BuilderTest.__init__")
    @patch("src.builder.os.walk")
    def test_find_tests(self, mock_walk: Mock, mock__init__: Mock) -> None:
        mock__init__.return_value = None
        mock_walk.return_value.__iter__.return_value = [
            (PATH_OF_DATA + "/1/1", None, ["first.json"]),
            (PATH_OF_DATA + "/2/2", None, ["my_test.json"]),
            (PATH_OF_DATA + "/1/2", None, ["first.json"]),
        ]

        assert BuilderTest()._find_tests() == [
            (1, 1, PATH_OF_DATA + "/1/1/first.json"),
            (2, 2, PATH_OF_DATA + "/2/2/my_test.json"),
            (1, 2, PATH_OF_DATA + "/1/2/first.json"),
        ]


@patch("src.builder.Test.__init__", return_value=None)
@patch("src.builder.User.add_test")
@patch("src.builder.BuilderTest._find_tests")
@patch("src.builder.BuilderTest._append_tests_to_tree")
@patch("src.builder.BuilderTest._initialize_test")
@patch("src.builder.BuilderTest._read_file")
@patch("src.builder.BuilderTest.__init__", return_value=None)
@patch("src.builder.cpu_count")
class TestCreateTestsFromFiles:
    def test_if_cpu_count_equals_one(
        self,
        mock_cpu_count: Mock,
        mock__init__: Mock,
        mock_read_file: Mock,
        mock_initialize_test: Mock,
        mock_append_tests_to_tree: Mock,
        mock_find_tests: Mock,
        mock_add_test: Mock,
        mock_test__init__: Mock,
    ) -> None:
        mock_cpu_count.return_value = 1
        mock_find_tests.return_value = [(1, 2, PATH_OF_DATA + "/1/1/test.json")]

        def _mock_read_file(
            content: list[tuple[int, int, str]],
            errors: list[Union[str, int]],
            from_user_id: int,
            number: int,
            file_name: str,
            is_raised: bool = False,
        ) -> None:
            content.append((from_user_id, number, '{"command": "/test_test"}'))
            return

        class_ = Test("", "", None, [], None)
        class_._command = "0"

        def _mock_initialize_test(
            initialized_tests: list[tuple[int, int, Test]],
            from_user_id: int,
            number: int,
            file_content: dict[str, Any],
        ) -> None:
            initialized_tests.append((from_user_id, number, class_))
            return

        mock_read_file.side_effect = _mock_read_file
        mock_initialize_test.side_effect = _mock_initialize_test

        BuilderTest()._create_tests_from_files()

        mock_add_test.assert_called_once_with(1, 2, "0")
        mock_append_tests_to_tree.assert_called_once_with([(1, 2, class_)])

    @patch("src.builder.Manager")
    @patch("src.builder.Pool")
    def test_if_cpu_count_greater_than_one(
        self,
        mock_pool: Mock,
        mock_manager: Mock,
        mock_cpu_count: Mock,
        mock__init__: Mock,
        mock_read_file: Mock,
        mock_initialize_test: Mock,
        mock_append_tests_to_tree: Mock,
        mock_find_tests: Mock,
        mock_add_test: Mock,
        mock_test__init__: Mock,
    ) -> None:
        mock_cpu_count.return_value = 2
        mock_find_tests.return_value = [(1, 2, PATH_OF_DATA + "/1/1/test.json")]
        mock_manager.return_value.__enter__.return_value.list.side_effect = [[], []]

        def mock_pool_map(func: Callable[[], Any], iterable: Iterable[Any]) -> None:
            for element in iterable:
                func(*element)

        class_ = Test("", "", None, [], None)
        class_._command = "0"

        def _mock_read_file(
            content: list[tuple[int, int, str]],
            errors: list[Union[str, int]],
            from_user_id: int,
            number: int,
            file_name: str,
            is_raised: bool = False,
        ) -> None:
            content.append((from_user_id, number, '{"command": "/test_test"}'))
            return

        def _mock_initialize_test(
            initialized_tests: list[tuple[int, int, object]],
            from_user_id: int,
            number: int,
            file_content: dict[str, Any],
        ) -> None:
            initialized_tests.append((from_user_id, number, class_))
            return

        mock_read_file.side_effect = _mock_read_file
        mock_initialize_test.side_effect = _mock_initialize_test

        mock_pool.return_value.__enter__.return_value.starmap = mock_pool_map

        BuilderTest()._create_tests_from_files()
        mock_add_test.assert_called_once_with(1, 2, "0")
        mock_append_tests_to_tree.assert_called_once_with([(1, 2, class_)])


@patch("src.builder.open")
@patch("src.builder.BuilderTest.__init__")
class TestReadFile:
    def test_json_right(self, mock__init__: Mock, mock_open: Mock) -> None:
        mock__init__.return_value = None
        mock_open.return_value.__enter__.return_value.read.return_value = (
            '{"command": "test_test"}'
        )

        files_content: list[tuple[int, int, dict[str, Any]]] = []
        BuilderTest()._read_file(files_content, [], 1, 2, "name")

        assert files_content == [(1, 2, {"command": "test_test"})]

    def test_json_wrong(self, mock__init__: Mock, mock_open: Mock) -> None:
        mock__init__.return_value = None
        mock_open.return_value.__enter__.return_value.read.return_value = (
            '"command": "test_test"'
        )

        files_content: list[tuple[int, int, dict[str, Any]]] = []

        with pytest.raises(JSONDecodeError):
            BuilderTest()._read_file(files_content, [], 1, 2, "name")


@patch("src.builder.Question.__init__")
@patch("src.builder.Test.__init__")
@patch("src.builder.BuilderTest.__init__")
class TestInitializeTest:
    def test_initialized(
        self,
        mock_builder__init__: Mock,
        mock_test__init__: Mock,
        mock_question__init__: Mock,
    ) -> None:
        mock_test__init__.return_value = None
        mock_question__init__.return_value = None
        mock_builder__init__.return_value = None

        file_content = {
            "command": "/test_Romanovy",
            "name": "Романовы",
            "description": "Тест про царей и императоров Романовых.",
            "questions": [
                {
                    "body": "Какое было имя у первого царя в семействе Романовых",
                    "widget": {"type": "input"},
                    "answer": "Михаил",
                    "answer_explanation": "",
                },
                {
                    "body": "Как звали первого императора в семействе романовых",
                    "widget": {
                        "type": "button",
                        "body": [
                            "Петр I",
                            "Алексей Михайлович",
                            "Николай I",
                            "Михаил Фёдорович",
                        ],
                    },
                    "answer": 1,
                    "answer_explanation": "Первым императором был Петр I.",
                },
            ],
            "result_explanation": {"2": "Хорошо", "0": "Плохо"},
        }

        initialized_tests: list[tuple[int, int, Test]] = []
        BuilderTest()._initialize_test(initialized_tests, 1, 2, file_content)

        questions: Any = file_content["questions"]
        mock_question__init__.assert_has_calls(
            [call(*args.values()) for args in questions]
        )

        mock_test__init__.assert_called_once()
        assert mock_test__init__.mock_calls[0].args[0] == file_content["command"]
        assert mock_test__init__.mock_calls[0].args[1] == file_content["name"]
        assert mock_test__init__.mock_calls[0].args[2] == file_content["description"]
        for question in mock_test__init__.mock_calls[0].args[3]:
            assert isinstance(question, Question)
        assert (
            mock_test__init__.mock_calls[0].args[4]
            == file_content["result_explanation"]
        )

        assert initialized_tests[0][0] == 1
        assert initialized_tests[0][1] == 2
        assert isinstance(initialized_tests[0][2], Test)


@patch("src.builder.Validator.__init__")
@patch("src.builder.BuilderTest.__init__")
class TestValidate:
    def test_validate(
        self, mock_builder__init__: Mock, mock_validator__init__: Mock
    ) -> None:
        mock_builder__init__.return_value = None
        mock_validator__init__.return_value = None
        file_content = {
            "command": "/test_Romanovy",
            "name": "Романовы",
            "description": "Тест про царей и императоров Романовых.",
            "questions": [
                {
                    "body": "Какое было имя у первого царя в семействе Романовых",
                    "widget": {"type": "input"},
                    "answer": "Михаил",
                    "answer_explanation": "",
                },
                {
                    "body": "Как звали первого императора в семействе романовых",
                    "widget": {
                        "type": "button",
                        "body": [
                            "Петр I",
                            "Алексей Михайлович",
                            "Николай I",
                            "Михаил Фёдорович",
                        ],
                    },
                    "answer": 1,
                    "answer_explanation": "Первым императором был Петр I.",
                },
            ],
            "result_explanation": {"2": "Хорошо", "0": "Плохо"},
        }
        errors: list[Union[str, int]] = []
        BuilderTest()._validate(file_content, errors)
        mock_validator__init__.assert_called_once_with(
            errors,
            file_content["command"],
            file_content["name"],
            file_content["description"],
            file_content["questions"],
            file_content["result_explanation"],
        )


@patch("src.builder.Test.__init__")
@patch("src.builder.CommandsTestTree.append")
@patch("src.builder.CommandsTestTree.__init__")
@patch("src.builder.BuilderTest.__init__")
class TestAppendTestsToTree:
    def test_append_tests_to_tree(
        self,
        mock_builder__init__: Mock,
        mock_tree__init__: Mock,
        mock_tree_append: Mock,
        mock_test__init__: Mock,
    ) -> None:
        mock_builder__init__.return_value = None
        mock_tree__init__.return_value = None
        mock_test__init__.return_value = None

        tests = [
            (0, 1, Test("", "", None, [], None)),
            (0, 1, Test("", "", None, [], None)),
            (0, 1, Test("", "", None, [], None)),
        ]
        BuilderTest()._append_tests_to_tree(tests)

        mock_arguments = mock_tree_append.mock_calls
        assert len(mock_arguments) == 3
        for mock_argument in mock_arguments:
            mock_argument = mock_argument.args[0]
            assert isinstance(mock_argument, Node)

            assert mock_argument.parent is None
            assert mock_argument.left is None
            assert mock_argument.right is None
            assert mock_argument.color is ColorTree.RED
            assert isinstance(mock_argument.key, Test)
