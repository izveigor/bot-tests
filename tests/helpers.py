import json
from typing import Any


class _JsonData:
    """Testing class of getting data from "data.json"
    To get test data from file, get attribute from instance of class (JsonData) with name of field.
    For example: JsonData.first_block_result (return clearing first block like a python dictionary)
    To get test data with json encoding, get attribute from instance of class (JsonData) with name of field + "_json".
    For example: JsonData.first_block_json (return first block like a json data).
    """

    _file_name = "tests/data.json"

    def __getattr__(self, name: str) -> Any:
        with open(self._file_name) as json_file:
            file_data = json_file.read()
            try:
                data: Any = json.loads(file_data)
            except json.decoder.JSONDecodeError as error:
                raise error
            try:
                if name.rfind("_json", -5) != -1:
                    return json.dumps(data[name[:-5]])
                else:
                    return data[name]
            except KeyError as e:
                raise e


JsonData = _JsonData()
