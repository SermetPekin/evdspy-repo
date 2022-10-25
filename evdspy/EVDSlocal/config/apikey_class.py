from ..common.common_imports import *
from dataclasses import dataclass
from typing import Union
from enum import Enum, auto
from ..config.config import config

class ApiKeyType(Enum):
    runtime = auto()
    from_file = auto()
    from_file_options = auto()


@dataclass
class ApiKeyValue:
    name: str
    value: Union[str, bool] = False
    type_: ApiKeyType = ApiKeyType.runtime


@dataclass
class ApiKeyDict:
    runtime_apikey: ApiKeyValue = ApiKeyValue("runtime", False, ApiKeyType.runtime)
    from_file_apikey: ApiKeyValue = ApiKeyValue("fromfile", False, ApiKeyType.from_file)
    from_file_options_api_key: ApiKeyValue = ApiKeyValue("fromfile_options", False, ApiKeyType.from_file_options)

    def set_value(self, type_: Union[str, ApiKeyType], value):
        if type_ in ["runtime", ApiKeyType.runtime]:
            self.runtime_apikey.value = value
            return
        if type_ in ["fromfile", ApiKeyType.from_file]:
            self.from_file_apikey.value = value
            return
        self.from_file_options_api_key = value


class ApikeyClass(object):
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(ApikeyClass, cls).__new__(cls)
            cls.post_init(cls)
        return cls.instance

    def __repr__(cls):
        return f"""
   cls.now_testing_is_key_is_valid: {cls.now_testing_is_key_is_valid:}
   cls.current_key_using : {cls.current_key_using}
   cls.APIKEYDict : {cls.APIKEYDict}
"""

    def post_init(cls):

        cls.APIKEYDict: ApiKeyDict = ApiKeyDict()
        cls.now_testing_is_key_is_valid: Union[str, bool] = False
        cls.current_key_using: Union[str, bool] = cls.APIKEYDict.runtime_apikey.value

    def get_valid_api_key(cls):

        if config.current_mode_is_test:
            return "VALID_KEY_FOR_TEST"

        if cls.now_testing_is_key_is_valid:
            return cls.now_testing_is_key_is_valid

        key_objs = cls.get_api_keys()
        if not key_objs:
            return False
        return key_objs[0].value

    def set_api_key_runtime(cls, value: str):
        cls.instance.APIKEYDict.set_value(ApiKeyType.runtime, value)
        return cls.instance.APIKEYDict.runtime_apikey.value

    def set_api_key_filetype(cls, value: str):
        cls.instance.APIKEYDict.set_value(ApiKeyType.from_file, value)

        return cls.instance.APIKEYDict.from_file_apikey.value

    def set_api(cls, key: str):
        print("set api not implemented")
        raise "set api not implemented"

    def get_api_keys(cls):
        keys = [
            cls.instance.APIKEYDict.runtime_apikey,
            cls.instance.APIKEYDict.from_file_apikey,
            cls.instance.APIKEYDict.from_file_options_api_key,
        ]
        return [x for x in keys if x.value is not False]

    def get_api_keys_dict(cls):
        return cls.instance.APIKEYDict

    def get_api_key_runtime(cls):
        return cls.instance.APIKEYDict.runtime_apikey.value

    def get_api_key_fromfile(cls):
        return cls.instance.APIKEYDict.from_file_apikey.value

    def get_api_key_fromfile_options(cls):
        return cls.instance.APIKEYDict.from_file_options_api_key.value
