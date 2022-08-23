import os
import re
from typing import Any

PATH_OF_DATA = "src/data"


WIDGET_TYPES = ("input", "button", "checkbox")


REGEX_COMMAND = re.compile(r"^/test_[a-zA-Z0-9_]{1,35}$")
REGEX_FILE = re.compile(r"^[a-zA-Z0-9_-]+\.json$")
REGEX_LIST = re.compile(r"^/list [0-9]+-[0-9]+$")

REDIS_SETTINGS: dict[str, Any] = {
    "host": os.environ.get("REDIS_HOST"),
    "port": os.environ.get("REDIS_PORT"),
    "encoding": "utf-8",
    "decode_responses": True,
}
