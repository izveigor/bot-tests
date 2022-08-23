from typing import Any, Generator

import pytest
from pytest import Config

from src.tree import CommandsTestTree


@pytest.fixture(scope="function")
def patch_singleton(monkeypatch: Config) -> Generator[Any, Any, Any]:
    monkeypatch.setattr(CommandsTestTree.__class__, "_instances", {})
    yield
