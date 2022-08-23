import re
from typing import Any, Optional, Union
from unittest.mock import Mock, call, patch

import pytest

from src.constants import WIDGET_TYPES
from src.errors import BotParseException
from src.tree import Node
from src.validate import Validator, _QuestionValidator, _WidgetValidator
from tests.helpers import JsonData


class TestValidator:
    @patch("src.validate.Validator._is_result_explanation_right")
    @patch("src.validate.Validator._are_questions_right")
    @patch("src.validate.Validator._is_description_right")
    @patch("src.validate.Validator._is_name_right")
    @patch("src.validate.Validator._is_command_right")
    def test__init__(
        self,
        mock_is_command_right: Mock,
        mock_is_name_right: Mock,
        mock_is_description_right: Mock,
        mock_are_questions_right: Mock,
        mock_is_result_explanation_right: Mock,
    ) -> None:
        test = JsonData.validate_right[0]

        command = test["command"]
        name = test["name"]
        description = test["description"]
        questions = test["questions"]
        result_explanation = test["result_explanation"]
        errors: list[Union[str, int]] = []

        Validator(errors, command, name, description, questions, result_explanation)
        mock_is_command_right.assert_called_once_with(command, errors)
        mock_is_name_right.assert_called_once_with(name, errors)
        mock_is_description_right.assert_called_once_with(description, errors)
        mock_are_questions_right.assert_called_once_with(questions, errors)
        mock_is_result_explanation_right.assert_called_once_with(
            result_explanation, len(questions), errors
        )


@patch("src.validate.CommandsTestTree.search", return_value=None)
class TestIsCommandRight:
    @pytest.mark.parametrize(
        ("command"),
        [
            ("/test_Romanovy"),
            ("/test_dinosaur"),
            ("/test_0"),
            ("/test_" + "0" * 35),
        ],
    )
    def test_right(self, mock_search: Mock, command: str) -> None:
        Validator._is_command_right(command, [])
        assert isinstance(mock_search.mock_calls[0].args[0], Node)

    @pytest.mark.parametrize(
        ("command", "error"),
        [
            ({"test": "failed"}, "Команда должна быть непустой строкой."),
            ("", "Команда должна быть непустой строкой."),
            ("test_Romanovy", r"Команда не подходит под заданный шаблон.+"),
            ("test_РусскийЯзык", r"Команда не подходит под заданный шаблон.+"),
            ("test_Moon and Earth", r"Команда не подходит под заданный шаблон.+"),
            ("NewTest", r"Команда не подходит под заданный шаблон.+"),
            ("test", r"Команда не подходит под заданный шаблон.+"),
            ("test_" + "0" * 36, r"Команда не подходит под заданный шаблон.+"),
        ],
    )
    def test_error(self, mock_search: Mock, command: str, error: str) -> None:
        errors: list[Union[str, int]] = []
        with pytest.raises(
            BotParseException,
        ):
            Validator._is_command_right(command, errors)
        assert re.match(error, str(errors[0]))

    def test_if_command_exist(self, mock_search: Mock) -> None:
        mock_search.return_value = "Тест найден!"
        command = "/test_duplicate"
        error = "Тест с такой командой уже существует."
        errors: list[Union[str, int]] = []

        with pytest.raises(BotParseException):
            Validator._is_command_right(command, errors)
        assert re.match(error, str(errors[0]))


class TestIsNameRight:
    """Тест на валидацию имени теста."""

    @pytest.mark.parametrize(
        ("name"),
        [
            ("Нормальное имя"),
            ("0" * 30),
        ],
    )
    def test_right(self, name: str) -> None:
        Validator._is_name_right(name, [])

    @pytest.mark.parametrize(
        ("name", "error"),
        [
            ({"test": "failed"}, "Название теста должно быть непустой строкой."),
            ("", "Название теста должно быть непустой строкой."),
            ("0" * 31, "Количество символов в название теста не может превышать 30."),
        ],
    )
    def test_error(self, name: Any, error: str) -> None:
        errors: list[Union[str, int]] = []
        with pytest.raises(
            BotParseException,
        ):
            Validator._is_name_right(name, errors)
        assert re.match(error, str(errors[0]))


class TestIsDescriptionRight:
    @pytest.mark.parametrize(
        ("description"),
        [
            ("Описание теста."),
            (None),
            ("0" * 900),
            ({"text": "Описание теста."}),
            ({"text": None}),
            ({"url": None}),
            ({"url": "earth.jpg", "text": "Тест про Землю."}),
        ],
    )
    def test_right(self, description: str) -> None:
        Validator._is_description_right(description, [])

    @pytest.mark.parametrize(
        ("description", "error"),
        [
            (
                ["test", "failed"],
                "Описание должно быть либо строкой, либо пустым значением.",
            ),
            (
                "0" * 901,
                "Количество символов в тексте описания теста не должно превышать 900.",
            ),
            (
                {"text": "0" * 901},
                "Количество символов в тексте описания теста не должно превышать 900.",
            ),
            (
                {"text": ["test", "failed"]},
                "Описание должно быть либо строкой, либо пустым значением, либо словарём со строковым или пустым значением text.",
            ),
            (
                {"url": {"test": "failed"}},
                "URL рисунка должно быть либо строкой, либо пустым значением.",
            ),
        ],
    )
    def test_error(self, description: Any, error: str) -> None:
        errors: list[Union[str, int]] = []
        with pytest.raises(
            BotParseException,
        ):
            Validator._is_description_right(description, errors)
        assert re.match(error, str(errors[0]))


@patch("src.validate._QuestionValidator.__init__", return_value=None)
class TestAreQuestionsRight:
    @pytest.mark.parametrize(
        ("questions"),
        [
            (
                [
                    {
                        "body": "Вопрос",
                        "answer": "Ответ",
                    }
                ]
            )
        ],
    )
    def test_right(
        self, mock_question_validator__init__: Mock, questions: list[dict[str, Any]]
    ) -> None:
        Validator._are_questions_right(questions, [])

    @pytest.mark.parametrize(
        ("questions", "error"),
        [
            ({"body": "failed"}, "Вопросы теста должны быть непустым списком."),
            ([], "Вопросы теста должны быть непустым списком."),
            (
                [
                    {
                        "body": "Вопрос",
                        "answer": "Ответ",
                    },
                    2,
                    3,
                ],
                "2-й вопрос не является словарем.",
            ),
        ],
    )
    def test_error(
        self, mock_question_validator__init__: Mock, questions: Any, error: str
    ) -> None:
        errors: list[Union[str, int]] = []
        with pytest.raises(
            BotParseException,
        ):
            Validator._are_questions_right(questions, errors)
        assert re.match(error, str(errors[0]))


class TestIsResultExplanationRight:
    @pytest.mark.parametrize(
        ("result_explanation", "questions_length"),
        [
            (None, 1),
            ({}, 1),
            ({"0": "0", "1": "1", "2": "2"}, 2),
            ({"0": "0", "4": "4"}, 5),
            ({"0": {"text": "0" * 900}}, 1),
        ],
    )
    def test_right(
        self, result_explanation: Optional[dict[str, Any]], questions_length: int
    ) -> None:
        Validator._is_result_explanation_right(result_explanation, questions_length, [])

    @pytest.mark.parametrize(
        ("result_explanation", "questions_length", "error"),
        [
            (
                {"0": "text", "key": "text"},
                3,
                r"2-ый ключ объяснения промежутка результата не принадлежит +",
            ),
            (
                {"0": "0", "1": "1", "3": "3", "2": "2"},
                2,
                "3-ый ключ объяснения промежутка результата не принадлежит промежутку от 0 до 2.",
            ),
            (
                {"0": "0", "-1": "-1"},
                1,
                "2-ый ключ объяснения промежутка результата не принадлежит промежутку от 0 до 1.",
            ),
            (
                {"0": "0" * 901},
                1,
                "Количество символов в тексте объяснения промежутка результата не должно превышать 900.",
            ),
            (
                {"0": {"text": "0" * 901}},
                1,
                "Количество символов в тексте объяснения промежутка результата не должно превышать 900.",
            ),
            (
                {"0": {"url": [1, 2]}},
                1,
                "URL рисунка должно быть либо строкой, либо пустым значением.",
            ),
            (
                {"0": {"text": {"test": "failed"}}},
                1,
                "Объяснение промежутка результата должно быть либо строкой, либо пустым значением, либо словарем со строковым или пустым значением text.",
            ),
            (
                [],
                1,
                "Объяснение промежутка результата должно быть либо строкой, либо пустым значением, либо словарем со строковым или пустым значением text.",
            ),
            (
                {"0": []},
                1,
                "Объяснение промежутка результата должно быть либо строкой, либо пустым значением, либо словарем со строковым или пустым значением text.",
            ),
        ],
    )
    def test_error(
        self, result_explanation: Any, questions_length: int, error: str
    ) -> None:
        errors: list[Union[str, int]] = []
        with pytest.raises(
            BotParseException,
        ):
            Validator._is_result_explanation_right(
                result_explanation, questions_length, errors
            )
        assert re.match(error, str(errors[0]))


class TestQuestionValidator:
    @patch("src.validate._QuestionValidator._is_answer_explanation_right")
    @patch("src.validate._QuestionValidator._is_answer_right")
    @patch("src.validate._QuestionValidator._is_widget_right")
    @patch("src.validate._QuestionValidator._is_body_right")
    def test__init__(
        self,
        mock_is_body_right: Mock,
        mock_is_widget_right: Mock,
        mock_is_answer_right: Mock,
        mock_is_answer_explanation_right: Mock,
    ) -> None:
        questions = JsonData.validate_right[0]["questions"]

        body_calls = []
        widget_calls = []
        answer_calls = []
        answer_explanation_calls = []

        for question in questions:
            body = question["body"]
            widget = question.get("widget")
            answer = question["answer"]
            answer_explanation = question.get("answer_explanation")
            errors: list[Union[str, int]] = []

            _QuestionValidator(errors, body, widget, answer, answer_explanation)

            body_calls.append(call(body, errors))
            widget_calls.append(call(widget, errors))
            answer_calls.append(call(answer, widget, errors))
            answer_explanation_calls.append(call(answer_explanation, errors))

        mock_is_body_right.assert_has_calls(body_calls)
        mock_is_widget_right.assert_has_calls(widget_calls)
        mock_is_answer_right.assert_has_calls(answer_calls)
        mock_is_answer_explanation_right.assert_has_calls(answer_explanation_calls)


class TestIsBodyQuestionRight:
    @pytest.mark.parametrize(
        ("body"),
        [
            ("Как звали первого российского императора?"),
            ("0" * 900),
            ({"text": "Как звали первого российского императора?"}),
            ({"url": "moon.png", "text": "Что изображено на картинке?"}),
        ],
    )
    def test_right(self, body: Union[str, dict[str, str]]) -> None:
        _QuestionValidator._is_body_right(body, [])

    @pytest.mark.parametrize(
        ("body", "error"),
        [
            (
                ["test", "failed"],
                "Тело вопроса должно быть либо непустой строкой, либо непустым словарем с непустой строкой text.",
            ),
            (
                "",
                "Тело вопроса должно быть либо непустой строкой, либо непустым словарем с непустой строкой text.",
            ),
            (
                "0" * 901,
                "Количество символов в тексте тела вопроса не должно превышать 900.",
            ),
            (
                {"text": [1, 2]},
                "Тело вопроса должно быть либо непустой строкой, либо непустым словарем с непустой строкой text.",
            ),
            (
                {"text": "0" * 901},
                "Количество символов в тексте тела вопроса не должно превышать 900.",
            ),
            (
                {"text": ""},
                "Тело вопроса должно быть либо непустой строкой, либо непустым словарем с непустой строкой text.",
            ),
            (
                {"url": [1, 2], "text": "text"},
                "URL рисунка должно быть либо строкой, либо пустым значением.",
            ),
        ],
    )
    def test_error(self, body: Any, error: str) -> None:
        errors: list[Union[str, int]] = []
        with pytest.raises(
            BotParseException,
        ):
            _QuestionValidator._is_body_right(body, errors)
        assert re.match(error, str(errors[0]))


@patch("src.validate._WidgetValidator.__init__", return_value=None)
class TestIsWidgetRight:
    @pytest.mark.parametrize(
        ("widget"),
        [
            ({"type": "button", "body": ["Yes", "No"]}),
            (None),
        ],
    )
    def test_right(
        self, mock_widget_validator__init__: Mock, widget: Optional[dict[str, Any]]
    ) -> None:
        errors: list[Union[str, int]] = []
        _QuestionValidator._is_widget_right(widget, errors)
        if widget is not None:
            mock_widget_validator__init__.assert_called_once_with(
                errors, widget["type"], widget["body"]
            )
        else:
            mock_widget_validator__init__.assert_not_called()

    @pytest.mark.parametrize(
        ("widget", "error"),
        [
            (
                [1, 2, 3],
                "Элемент интерфейса должен быть либо словарем, либо пустым значением.",
            ),
        ],
    )
    def test_if_widget_is_not_None_or_dict(
        self, mock_widget_validator: Mock, widget: Any, error: str
    ) -> None:
        errors: list[Union[str, int]] = []
        with pytest.raises(
            BotParseException,
        ):
            _QuestionValidator._is_widget_right(widget, errors)
        assert re.match(error, str(errors[0]))


class TestIsAnswerRight:
    @pytest.mark.parametrize(
        ("answer", "widget"),
        [
            ("Правильный ответ", {"type": "input"}),
            (1, {"type": "button", "body": {"Yes", "No"}}),
            (2, {"type": "button", "body": {"Yes", "No"}}),
            ([2, 3], {"type": "checkbox", "body": {"1", "2", "3", "4"}}),
            ("Правильный ответ", {}),
            ("0" * 40, None),
        ],
    )
    def test_right(
        self, answer: Union[str, int, list[int]], widget: Optional[dict[str, Any]]
    ) -> None:
        _QuestionValidator._is_answer_right(answer, widget, [])

    @pytest.mark.parametrize(
        ("answer", "widget", "error"),
        [
            (
                {"test": "failed"},
                {"type": "input"},
                "Используемый элемент интерфейса является полем редактированием, ответ должен быть непустой строкой.",
            ),
            (
                "",
                {"type": "input"},
                "Используемый элемент интерфейса является полем редактированием, ответ должен быть непустой строкой.",
            ),
            (
                "0" * 41,
                None,
                "Используемый элемент интерфейса является полем редактированием, количество символов в ответе не должно превышать 40.",
            ),
            (
                "Правильный ответ",
                {"type": "button", "body": ["Yes", "No"]},
                "Используемый элемент интерфейса является кнопкой, ответ должен принадлежать целочисленному типу данных.",
            ),
            (
                0,
                {"type": "button", "body": ["Yes", "No"]},
                "Используемый элемент интерфейса является кнопкой, ответ должен варьироваться от 1 до 2.",
            ),
            (
                3,
                {"type": "button", "body": ["Yes", "No"]},
                "Используемый элемент интерфейса является кнопкой, ответ должен варьироваться от 1 до 2.",
            ),
            (
                {"test": "failed"},
                {"type": "checkbox", "body": ["1", "2", "3", "4"]},
                "Используемый элемент интерфейса является флаговой кнопкой, ответ должен быть непустым списком.",
            ),
            (
                [],
                {"type": "checkbox", "body": ["1", "2", "3", "4"]},
                "Используемый элемент интерфейса является флаговой кнопкой, ответ должен быть непустым списком.",
            ),
            (
                [1, {"test": "failed"}, 3],
                {"type": "checkbox", "body": ["1", "2", "3", "4"]},
                "Используемый элемент интерфейса является флаговой кнопкой, 2-ое включенное состояние не принадлежит целочисленному типу данных.",
            ),
            (
                [1, 2, 3, 4, 1],
                {"type": "checkbox", "body": ["1", "2", "3", "4"]},
                "Используемый элемент интерфейса является флаговой кнопкой, длина ответа не должна превышать тела элемента интерфейса.",
            ),
            (
                [1, 5],
                {"type": "checkbox", "body": ["1", "2", "3", "4"]},
                "Используемый элемент интерфейса является флаговой кнопкой, 2-ое включенное состояние не принадлежит промежутку от 1 до 4.",
            ),
            (
                [1, 1, 2, 2],
                {"type": "checkbox", "body": ["1", "2", "3", "4"]},
                "Используемый элемент интерфейса является флаговой кнопкой, в ответе присутствуют дубликаты следующих чисел: \[1, 2\].",
            ),
        ],
    )
    def test_error(
        self, answer: Any, widget: Optional[dict[str, Any]], error: str
    ) -> None:
        errors: list[Union[str, int]] = []
        with pytest.raises(
            BotParseException,
        ):
            _QuestionValidator._is_answer_right(answer, widget, errors)
        assert re.match(error, str(errors[0]))


class TestIsAnswerExplanationRight:
    @pytest.mark.parametrize(
        ("answer_explanation"),
        [
            (
                "Последним русским императором был Николай II. Он отрёкся от престола в 1917 году в результате Февральской революции."
            ),
            ("0" * 900),
            (None),
            ({"text": "text"}),
            ({"text": "0" * 900}),
            ({"url": "smile.png"}),
            ({"text": "text", "url": "smile.jpg"}),
        ],
    )
    def test_right(
        self, answer_explanation: Optional[Union[str, dict[str, str]]]
    ) -> None:
        _QuestionValidator._is_answer_explanation_right(answer_explanation, [])

    @pytest.mark.parametrize(
        ("answer_explanation", "error"),
        [
            (
                ["test", "failed"],
                "Объяснение ответа может быть либо строкой, либо пустым значением, либо словарём с пустым или строковым значением text.",
            ),
            (
                "0" * 901,
                "Количество символов в объснение ответа не должно превышать 900.",
            ),
            (
                {"text": [1, 2]},
                "Объяснение ответа может быть либо строкой, либо пустым значением, либо словарём с пустым или строковым значением text.",
            ),
            (
                {"text": "0" * 901},
                "Количество символов в объснение ответа не должно превышать 900.",
            ),
            (
                {"url": [1, 2]},
                "URL рисунка должно быть либо строкой, либо пустым значением.",
            ),
        ],
    )
    def test_error(self, answer_explanation: Any, error: str) -> None:
        errors: list[Union[str, int]] = []
        with pytest.raises(
            BotParseException,
        ):
            _QuestionValidator._is_answer_explanation_right(answer_explanation, errors)
        assert re.match(error, str(errors[0]))


class TestWidgetValidator:
    @patch("src.validate._WidgetValidator._is_body_right")
    @patch("src.validate._WidgetValidator._is_type_right")
    def test__init__(self, mock_is_type_right: Mock, mock_is_body_right: Mock) -> None:
        questions = JsonData.validate_right[0]["questions"]
        is_type_right_calls = []
        is_body_right_calls = []

        for question in questions:
            widget = question.get("widget")
            if widget is not None:
                widget_type = widget.get("type")
                body = widget.get("body")
                errors: list[Union[str, int]] = []

                _WidgetValidator(errors, widget_type, body)

                is_type_right_calls.append(call(widget_type, errors))
                is_body_right_calls.append(call(body, widget_type, errors))

        mock_is_type_right.assert_has_calls(is_type_right_calls)
        mock_is_body_right.assert_has_calls(is_body_right_calls)


class TestIsTypeRight:
    @pytest.mark.parametrize(
        ("widget_type"),
        [
            *((widget_type) for widget_type in WIDGET_TYPES),
            (None),
            (""),
        ],
    )
    def test_right(self, widget_type: Optional[str]) -> None:
        _WidgetValidator._is_type_right(widget_type, [])

    @pytest.mark.parametrize(
        ("widget_type", "error"),
        [
            (
                "Not input",
                'Тип пользовательского интерфейса "Not input" не является приемлемым.',
            ),
        ],
    )
    def test_error(self, widget_type: Any, error: str) -> None:
        errors: list[Union[str, int]] = []
        with pytest.raises(
            BotParseException,
        ):
            _WidgetValidator._is_type_right(widget_type, errors)
        assert re.match(error, str(errors[0]))


class TestIsBodyRight:
    @pytest.mark.parametrize(
        ("body", "widget_type"),
        [
            (None, "input"),
            (["Yes", "No"], "button"),
            (["1", "2", "3", "4"], "checkbox"),
            (["Yes", "0" * 40], "button"),
            (["Yes", "0" * 40, "No"], "checkbox"),
        ],
    )
    def test_right(self, body: Optional[list[str]], widget_type: str) -> None:
        _WidgetValidator._is_body_right(body, widget_type, [])

    @pytest.mark.parametrize(
        ("body", "widget_type", "error"),
        [
            (
                {"test": "failed"},
                "input",
                "Тело поля редактирования должно быть пустым.",
            ),
            ({"test": "failed"}, "button", "Тело кнопки должно быть непустым списком"),
            ([], "button", "Тело кнопки должно быть непустым списком"),
            (
                {"test": "failed"},
                "checkbox",
                "Тело флаговой кнопки должно быть непустым списком.",
            ),
            ([], "checkbox", "Тело флаговой кнопки должно быть непустым списком."),
            (
                ["Yes", {"test": "failed"}, "No"],
                "button",
                "Текст 2-ой кнопки должен быть непустой строкой.",
            ),
            (["", "Yes"], "button", "Текст 1-ой кнопки должен быть непустой строкой."),
            (
                ["Yes", {"test": "failed"}],
                "checkbox",
                "Текст 2-ой флаговой кнопки должен быть непустой строкой.",
            ),
            (
                ["Yes", "No", {"test": "failed"}],
                "checkbox",
                "Текст 3-ой флаговой кнопки должен быть непустой строкой.",
            ),
            (
                ["Yes", "0" * 41],
                "button",
                "Количество символов текста 2-ой кнопки не должно превышать 40 символов",
            ),
            (
                ["Yes", "0" * 41, "No"],
                "checkbox",
                "Количество символов текста 2-ой флаговой кнопки не должно превышать 40 символов.",
            ),
            (
                ["1", "2", "3", "4", "5"],
                "button",
                "Тело кнопки должно содержать не более 4 элементов.",
            ),
            (
                ["1", "2", "3", "4", "5"],
                "checkbox",
                "Тело флаговой кнопки должно содержать не более 4 элементов.",
            ),
        ],
    )
    def test_error(self, body: Any, widget_type: str, error: str) -> None:
        errors: list[Union[str, int]] = []
        with pytest.raises(
            BotParseException,
        ):
            _WidgetValidator._is_body_right(body, widget_type, errors)
        assert re.match(error, str(errors[0]))
