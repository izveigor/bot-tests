"""В этом модуле присутствуют все валидаторы, необходимые для проверки данных для тестов.

Классы:
    - Validator - открытый класс, который проверяет все данные
    - _QuestionValidator - закрытый класс, который проверяет поля вопроса (вызывается Validator)
    - _WidgetValidator - закрытый класс, проверяет поля элемента интерфейса (вызывается Validator)
"""

from typing import Any, Union

from .constants import REGEX_COMMAND, WIDGET_TYPES
from .errors import BotParseException
from .test import Test
from .tree import CommandsTestTree, Node


class Validator:
    """Валидатор для тестов.

    Данные, извлеченные из тестов, проверяются с помощью вызова конструктора этого класса.
    """

    def __init__(
        self,
        errors: list[Union[str, int]],
        command: Any,
        name: Any,
        description: Any,
        questions: Any,
        result_explanation: Any,
    ) -> None:
        """Проверяет правильность всех команд.

        Аргументы:
            errors - список ошибок
            command - поле "Команда"
            name - поле "Название"
            description - поле "Описание"
            questions - поле "Вопросы"
            result_explanation - поле "Объяснение результата"
        Возвращает: None
        """
        self._is_command_right(command, errors)
        self._is_name_right(name, errors)
        self._is_description_right(description, errors)
        self._are_questions_right(questions, errors)
        self._is_result_explanation_right(result_explanation, len(questions), errors)

    @staticmethod
    def _is_command_right(command: Any, errors: list[Union[str, int]]) -> None:
        """Проверяет правильность поля "Команда".

        Аргументы:
            command - поле "Команда"
            errors - список ошибок
        Возвращает: None
        Вызывает: BotParseException, если:
            - Команда не является непустой строкой
            - Команда не подходит под заданный шаблон
            - Команда уже была использована другим тестом
        """
        if not isinstance(command, str) or not command:
            raise BotParseException(errors, "Команда должна быть непустой строкой.")

        if not REGEX_COMMAND.match(command):
            raise BotParseException(
                errors,
                'Команда не подходит под заданный шаблон. В начале должно стоять слово "test_". Далее к нему приписываются все буквы латинского алфавита (прописные и/или строчные) и/или десятичные цифры и/или _. Максимальная длина команды с учетом начального слова не должна превышать 40.',
            )

        if (
            CommandsTestTree().search(Node(Test(command, "", None, [], None)))
            is not None
        ):
            raise BotParseException(errors, "Тест с такой командой уже существует.")

    @staticmethod
    def _is_name_right(name: Any, errors: list[Union[str, int]]) -> None:
        """Проверяет правильность поля "Название".

        Аргументы:
            name - поле "Название"
            errors - список ошибок
        Возвращает: None
        Вызывает: BotParseException, если:
            - Название не является непустой строкой
            - В название больше 30 символов
        """
        if not isinstance(name, str) or not name:
            raise BotParseException(
                errors, "Название теста должно быть непустой строкой."
            )

        if len(name) > 30:
            raise BotParseException(
                errors,
                "Количество символов в название теста не может превышать 30.",
            )

    @staticmethod
    def _is_description_right(description: Any, errors: list[Union[str, int]]) -> None:
        """Проверяет правильность поля "Описание".

        Аргументы:
            description - поле "Описание"
            errors - список ошибок
        Возвращает: None
        Вызывает: BotParseException, если:
            Если описание является строкой:
                - Длина строки больше 900 символов
            Если описание является словарем:
                - Текст описания не пустое значение и не является строкой
                - Текст описания является строкой и количество символов в нем превышает 900.
                - URL рисунка не пустое значение и не является строкой
            - Описание не является словарем, пустым значением или строкой.
        """
        if isinstance(description, str):
            if len(description) > 900:
                raise BotParseException(
                    errors,
                    "Количество символов в тексте описания теста не должно превышать 900.",
                )
        elif isinstance(description, dict):
            url = description.get("url")
            text = description.get("text")

            if text and not isinstance(text, str):
                raise BotParseException(
                    errors,
                    "Описание должно быть либо строкой, либо пустым значением, либо словарём со строковым или пустым значением text.",
                )

            if text and len(text) > 900:
                raise BotParseException(
                    errors,
                    "Количество символов в тексте описания теста не должно превышать 900.",
                )

            if not (isinstance(url, str) or url is None):
                raise BotParseException(
                    errors,
                    "URL рисунка должно быть либо строкой, либо пустым значением.",
                )
        else:
            if description is not None:
                raise BotParseException(
                    errors,
                    "Описание должно быть либо строкой, либо пустым значением, либо словарём со строковым или пустым значением text.",
                )

    @staticmethod
    def _are_questions_right(questions: Any, errors: list[Union[str, int]]) -> None:
        """Проверяет правильность поля "Вопросы". В конце функции вызывает валидатор для проверки содержимого вопросов.

        Аргументы:
            questions - поле "Вопросы"
            errors - список ошибок
        Возвращает: None
        Вызывает: BotParseException, если:
            - Вопросы теста не являются непустым списком
            - В списке содержится вопрос, который не является словарем
        """
        if not isinstance(questions, list) or len(questions) == 0:
            raise BotParseException(
                errors, "Вопросы теста должны быть непустым списком."
            )

        for number, question in enumerate(questions, start=1):
            if not isinstance(question, dict):
                raise BotParseException(
                    errors, f"{number}-й вопрос не является словарем."
                )

            body = question.get("body")
            widget = question.get("widget")
            answer = question.get("answer")
            answer_description = question.get("answer_explanation")

            _QuestionValidator(
                errors,
                body,
                widget,
                answer,
                answer_description,
            )

    @staticmethod
    def _is_result_explanation_right(
        result_explanation: Any, questions_length: int, errors: list[Union[str, int]]
    ) -> None:
        """Проверяет правильность поля "Объяснение результата".

        Аргументы:
            result_explanation - поле "Объяснение результата"
            questions_length - длина списка вопросов
            errors - список ошибок
        Возвращает: None
        Вызывает: BotParseException, если:
            - Объяснение результата не является пустым значением или словарем.
            Если объяснение результата является словарем:
                - Ключ словаря не принадлежит целочисленному типу данных
                - Ключ словаря не принадлежит промежутку от 0 до длины списка вопросов
                Если значение является словарем:
                    - Текст объяснения промежутка вопроса не является пустым значением или строковым значением
                    - Текст является строковым значением и количество символов превышает 900
                    - URL рисунка не является пустым значением или строкой.
                Если значение является строкой:
                    - Количество символов в тексте превышает 900
                - Объяснение промежутка результата не является строкой, пустым значением или словарем
        """
        if isinstance(result_explanation, dict) and len(result_explanation) != 0:
            for number, (result_range, result_range_explanation) in enumerate(
                result_explanation.items(), start=1
            ):
                try:
                    result_range_int = int(result_range)
                except ValueError:
                    raise BotParseException(
                        errors,
                        '{0}-ый ключ объяснения промежутка результата не принадлежит целочисленному типу данных (Справка: в json формате все ключи записываются в виде строки, поэтому запись целочисленного типа данных должна выглядеть так: {{"0": "Текст"}}).'.format(
                            number
                        ),
                    )
                else:
                    if not (0 <= result_range_int <= questions_length):
                        raise BotParseException(
                            errors,
                            f"{number}-ый ключ объяснения промежутка результата не принадлежит промежутку от 0 до {questions_length}.",
                        )

                if isinstance(result_range_explanation, str):
                    if len(result_range_explanation) > 900:
                        raise BotParseException(
                            errors,
                            "Количество символов в тексте объяснения промежутка результата не должно превышать 900.",
                        )
                elif isinstance(result_range_explanation, dict):
                    url = result_range_explanation.get("url")
                    text = result_range_explanation.get("text")

                    if text and not isinstance(text, str):
                        raise BotParseException(
                            errors,
                            "Объяснение промежутка результата должно быть либо строкой, либо пустым значением, либо словарем со строковым или пустым значением text.",
                        )

                    if text and len(text) > 900:
                        raise BotParseException(
                            errors,
                            "Количество символов в тексте объяснения промежутка результата не должно превышать 900.",
                        )

                    if not (isinstance(url, str) or url is None):
                        raise BotParseException(
                            errors,
                            "URL рисунка должно быть либо строкой, либо пустым значением.",
                        )
                else:
                    raise BotParseException(
                        errors,
                        "Объяснение промежутка результата должно быть либо строкой, либо пустым значением, либо словарем со строковым или пустым значением text.",
                    )
        else:
            if not (
                result_explanation is None
                or isinstance(result_explanation, dict)
                and len(result_explanation) == 0
            ):
                raise BotParseException(
                    errors,
                    "Объяснение промежутка результата должно быть либо строкой, либо пустым значением, либо словарем со строковым или пустым значением text.",
                )


class _QuestionValidator:
    def __init__(
        self,
        errors: list[Union[str, int]],
        body: Any,
        widget: Any,
        answer: Any,
        answer_description: Any,
    ):
        self._is_body_right(body, errors)
        self._is_widget_right(widget, errors)
        self._is_answer_right(answer, widget, errors)
        self._is_answer_explanation_right(answer_description, errors)

    @staticmethod
    def _is_body_right(body: Any, errors: list[Union[str, int]]) -> None:
        """Проверяет правильность поля "Тела".

        Аргументы:
            body - поле "Тело"
            errors - список ошибок
        Возвращает: None
        Вызывает: BotParseException, если:
            Если тело вопроса является непустой строкой:
                - Количество символов в теле вопросов не должно превышать 900
            Если тело вопроса является словарем:
                - Текст тела вопроса должен быть непустой строкой
                - Количество символов в тексте тела вопроса не должно превышать 900
                - URL рисунка не является пустым значением или строкой
            - Тело вопроса не является непустой строкой или словарем
        """
        if body and isinstance(body, str):
            if len(body) > 900:
                raise BotParseException(
                    errors,
                    "Количество символов в тексте тела вопроса не должно превышать 900.",
                )
        elif isinstance(body, dict) and len(body) != 0:
            url = body.get("url")
            text = body.get("text")

            if not (text and isinstance(text, str)):
                raise BotParseException(
                    errors,
                    "Тело вопроса должно быть либо непустой строкой, либо непустым словарем с непустой строкой text.",
                )

            if len(text) > 900:
                raise BotParseException(
                    errors,
                    "Количество символов в тексте тела вопроса не должно превышать 900.",
                )

            if not (isinstance(url, str) or url is None):
                raise BotParseException(
                    errors,
                    "URL рисунка должно быть либо строкой, либо пустым значением.",
                )
        else:
            raise BotParseException(
                errors,
                "Тело вопроса должно быть либо непустой строкой, либо непустым словарем с непустой строкой text.",
            )

    @staticmethod
    def _is_widget_right(widget: Any, errors: list[Union[str, int]]) -> None:
        """Проверяет правильность поля "Элемент интерфейса". В конце функции вызывает валидатор для проверки содержимого элемента интерфейса.

        Аргументы:
            widget - поле "Элемент интерфейса"
            errors - список ошибок
        Возвращает: None
        Вызывает: BotParseException, если:
            - Элемент интерфейса не является словарем или пустым значением
        """
        if not (widget is None or isinstance(widget, dict)):
            raise BotParseException(
                errors,
                "Элемент интерфейса должен быть либо словарем, либо пустым значением.",
            )

        if widget is not None:
            widget_type = widget.get("type")
            body = widget.get("body")

            _WidgetValidator(errors, widget_type, body)

    @staticmethod
    def _is_answer_right(
        answer: Any, widget: Any, errors: list[Union[str, int]]
    ) -> None:
        """Проверяет правильность поля "Ответ".

        Аргументы:
            answer - поле "Ответ"
            widget - поле "Элемент интерфейса"
            errors - список ошибок
        Возвращает: None
        Вызывает: BotParseException, если:
            Если тип элемента интерфейса является полем редактирования:
                - Если ответ не является непустой строкой
                - Если количество символов в тексте ответа превышает 30
            Если тип элемента интерфейса является кнопкой:
                - Если ответ не принадлежит целочисленному типу данных
                - Если ответ не принадлежит промежутку от 1 до длины списка тела элемента интерфейса
            Если тип элемента интерфейса является флаговой кнопкой:
                - Ответ не является непустым списком
                - Длина списка больше длины списка тела элемента интерфейса
                - В списке содержится дубликаты чисел
                - Элемент списка не принаддежит целочисленному типу данных
                - Элемент списка не принадлежит промежутку от 1 до длины списка тела элемента интерфейса
            - Команда не подходит под заданный шаблон
            - Команда уже была использована другим тестом
        """
        widget_type = "input" if widget is None else widget.get("type", "input")

        if widget_type == "input":
            if not (answer and isinstance(answer, str)):
                raise BotParseException(
                    errors,
                    "Используемый элемент интерфейса является полем редактированием, ответ должен быть непустой строкой.",
                )

            if len(answer) > 40:
                raise BotParseException(
                    errors,
                    "Используемый элемент интерфейса является полем редактированием, количество символов в ответе не должно превышать 40.",
                )
        elif widget_type == "button":
            if not isinstance(answer, int):
                raise BotParseException(
                    errors,
                    "Используемый элемент интерфейса является кнопкой, ответ должен принадлежать целочисленному типу данных.",
                )

            body_length = len(widget.get("body"))

            if not 1 <= answer <= body_length:
                raise BotParseException(
                    errors,
                    f"Используемый элемент интерфейса является кнопкой, ответ должен варьироваться от 1 до {body_length}.",
                )
        elif widget_type == "checkbox":
            if not isinstance(answer, list) or len(answer) == 0:
                raise BotParseException(
                    errors,
                    "Используемый элемент интерфейса является флаговой кнопкой, ответ должен быть непустым списком.",
                )

            body_length = len(widget.get("body"))

            if len(answer) > body_length:
                raise BotParseException(
                    errors,
                    "Используемый элемент интерфейса является флаговой кнопкой, длина ответа не должна превышать тела элемента интерфейса.",
                )

            for number, checked in enumerate(answer, start=1):
                if not isinstance(checked, int):
                    raise BotParseException(
                        errors,
                        f"Используемый элемент интерфейса является флаговой кнопкой, {number}-ое включенное состояние не принадлежит целочисленному типу данных.",
                    )

                if not 1 <= checked <= body_length:
                    raise BotParseException(
                        errors,
                        f"Используемый элемент интерфейса является флаговой кнопкой, {number}-ое включенное состояние не принадлежит промежутку от 1 до {body_length}.",
                    )

            if len(set(answer)) != len(answer):
                duplicates = {
                    checked for checked in answer if answer.count(checked) > 1
                }
                raise BotParseException(
                    errors,
                    f"Используемый элемент интерфейса является флаговой кнопкой, в ответе присутствуют дубликаты следующих чисел: {list(duplicates)}.",
                )

    @staticmethod
    def _is_answer_explanation_right(
        answer_explanation: Any, errors: list[Union[str, int]]
    ) -> None:
        """Проверяет правильность поля "Объяснение ответа".

        Аргументы:
            answer_explanation - поле "Объяснение ответа"
            errors - список ошибок
        Возвращает: None
        Вызывает: BotParseException, если:
            Если объяснение ответа является строкой:
                - Количество символов первышает 900
            Если объяснение ответа является словарем:
                - Текст не является непустой строкой
                - Количество символов в тексте превышает 900
                - URL рисунка не является пустым значением или строкой
            - Объяснение ответа не является пустым значением, словарем или строкой.
        """
        if isinstance(answer_explanation, str):
            if len(answer_explanation) > 900:
                raise BotParseException(
                    errors,
                    "Количество символов в объснение ответа не должно превышать 900.",
                )
        elif isinstance(answer_explanation, dict):
            url = answer_explanation.get("url")
            text = answer_explanation.get("text")

            if text and not isinstance(text, str):
                raise BotParseException(
                    errors,
                    "Объяснение ответа может быть либо строкой, либо пустым значением, либо словарём с пустым или строковым значением text.",
                )

            if text and len(text) > 900:
                raise BotParseException(
                    errors,
                    "Количество символов в объснение ответа не должно превышать 900.",
                )

            if not (isinstance(url, str) or url is None):
                raise BotParseException(
                    errors,
                    "URL рисунка должно быть либо строкой, либо пустым значением.",
                )
        else:
            if answer_explanation is not None:
                raise BotParseException(
                    errors,
                    "Объяснение ответа может быть либо строкой, либо пустым значением, либо словарём с пустым или строковым значением text.",
                )


class _WidgetValidator:
    def __init__(
        self, errors: list[Union[str, int]], widget_type: Any, widget_body: Any
    ):
        self._is_type_right(widget_type, errors)
        self._is_body_right(widget_body, widget_type, errors)

    @staticmethod
    def _is_type_right(widget_type: Any, errors: list[Union[str, int]]) -> None:
        """Проверяет правильность поля "Тип элемента интерфейса".

        Аргументы:
            widget_type - поле "Тип элемент интерфейса"
            errors - список ошибок
        Возвращает: None
        Вызывает: BotParseException, если:
            - Тип элемента интерфейса не является пустым значением, "input", "button", "checkbox"
        """
        if widget_type and widget_type not in WIDGET_TYPES:
            raise BotParseException(
                errors,
                f'Тип пользовательского интерфейса "{widget_type}" не является приемлемым.',
            )

    @staticmethod
    def _is_body_right(
        widget_body: Any, widget_type: Any, errors: list[Union[str, int]]
    ) -> None:
        """Проверяет правильность поля "Тип элемента интерфейса".

        Аргументы:
            widget_body - полу "Тело элемента интерфейса"
            widget_type - поле "Тип элемент интерфейса"
            errors - список ошибок
        Возвращает: None
        Вызывает: BotParseException, если:
            Если тип элемента интерфейса является кнопкой или флаговой кнопкой:
                - Тело элемента интерфейса не является непустым списком
                - Длина тела превышает 4
                - Текст не является непустой строкой
                - Количество символов превышает 40
            Если тип элемента интерфейса является полем редактирования:
                - Тело не является пустым значением
        """
        if widget_type in ("button, checkbox"):

            if not isinstance(widget_body, list) or len(widget_body) == 0:
                if widget_type in "button":
                    raise BotParseException(
                        errors, "Тело кнопки должно быть непустым списком."
                    )
                else:
                    raise BotParseException(
                        errors,
                        "Тело флаговой кнопки должно быть непустым списком.",
                    )

            if len(widget_body) > 4:
                if widget_type in "button":
                    raise BotParseException(
                        errors,
                        "Тело кнопки должно содержать не более 4 элементов.",
                    )
                else:
                    raise BotParseException(
                        errors,
                        "Тело флаговой кнопки должно содержать не более 4 элементов.",
                    )

            for number, element_text in enumerate(widget_body, start=1):
                if not (element_text and isinstance(element_text, str)):
                    if widget_type in "button":
                        raise BotParseException(
                            errors,
                            f"Текст {number}-ой кнопки должен быть непустой строкой.",
                        )
                    else:
                        raise BotParseException(
                            errors,
                            f"Текст {number}-ой флаговой кнопки должен быть непустой строкой.",
                        )

                if len(element_text) > 40:
                    if widget_type == "button":
                        raise BotParseException(
                            errors,
                            f"Количество символов текста {number}-ой кнопки не должно превышать 40 символов.",
                        )
                    else:
                        raise BotParseException(
                            errors,
                            f"Количество символов текста {number}-ой флаговой кнопки не должно превышать 40 символов.",
                        )
        else:
            if widget_body is not None:
                raise BotParseException(
                    errors, "Тело поля редактирования должно быть пустым."
                )
