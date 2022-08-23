from unittest.mock import patch

import pytest
from fakeredis import FakeStrictRedis
from pytest import Config

from src.user import _User


@patch("src.user.redis.StrictRedis", FakeStrictRedis)
class TestActiveTest:
    def test_get_set_delete(self, patch_singleton: Config) -> None:
        User = _User()
        User.set(123, active_test="/test_test", question=2)
        assert User.get(123, "active_test") == "/test_test"
        assert User.get(123, "question") == "2"

        User.set(123, active_test="/test_another")
        assert User.get(123, "active_test") == "/test_another"
        assert User.get(123, "question") == "2"

        User.delete(123, "active_test", "question")
        with pytest.raises(
            ValueError,
        ):
            User.get(123, "active_test")
        with pytest.raises(
            ValueError,
        ):
            User.get(123, "question")

    def test_get_set_delete_test(self, patch_singleton: Config) -> None:
        User = _User()
        User.add_test(123, 2, "/test_test")
        assert User.get_tests_with_numbers(123) == [{"2": "/test_test"}]
        User.add_test(123, 1, "/test_user")
        assert User.get_tests_with_numbers(123) == [
            {"2": "/test_test"},
            {"1": "/test_user"},
        ]
        assert User.get_tests(123) == ["/test_test", "/test_user"]
        User.delete_test(123, "/test_user")
        assert User.get_tests(123) == ["/test_test"]
