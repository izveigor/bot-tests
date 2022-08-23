import re
from typing import Any, Union

import pytest

from src.errors import BotParseException
from src.validate import Validator
from tests.helpers import JsonData


@pytest.mark.parametrize(("data"), [(data) for data in JsonData.validate_right])
def test_Validator_without_exceptions(data: dict[str, Any]) -> None:
    command = data.get("command")
    name = data.get("name")
    description = data.get("description")
    questions = data.get("questions")
    result_explanation = data.get("result_explanation")

    errors: list[Union[str, int]] = []

    Validator(
        errors,
        command,
        name,
        description,
        questions,
        result_explanation,
    )


@pytest.mark.parametrize(
    ("data", "error"),
    [
        (list(validate_data.values())[0], list(validate_data.values())[1])
        for validate_data in JsonData.validate_wrong
    ],
)
def test_Validator_with_exceptions(
    data: dict[str, Any],
    error: str,
) -> None:
    command = data.get("command")
    name = data.get("name")
    description = data.get("description")
    questions = data.get("questions")
    result_explanation = data.get("result_explanation")

    errors: list[Union[str, int]] = []

    with pytest.raises(
        BotParseException,
    ):
        Validator(
            errors,
            command,
            name,
            description,
            questions,
            result_explanation,
        )

    re.match(error, str(errors[0]))
