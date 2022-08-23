from typing import Union

import pytest

from src.errors import BotFilesException, BotParseException


class TestErrors:
    def test_BotParseException(self) -> None:
        errors: list[Union[str, int]] = []
        with pytest.raises(BotParseException):
            raise BotParseException(errors, "message")
        assert errors[0] == "message"

    def test_BotFilesException(self) -> None:
        errors: list[Union[str, int]] = []
        with pytest.raises(BotFilesException):
            raise BotFilesException(errors, "message")
        assert errors[0] == "message"
