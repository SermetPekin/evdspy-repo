from ..common.common_imports import *
from dataclasses import dataclass, field
from typing import Union
from enum import Enum, auto
from ..config.config import config

from ..messages.error_classes import ApiKeyNotSetError


class ApiKeyType(Enum):
    runtime = auto()
    from_file = auto()
    from_file_options = auto()


@dataclass
class ApiKeyValue:
    name: str
    value: Union[str, bool] = False
    type_: ApiKeyType = ApiKeyType.runtime


class ApiKeyDict:
    runtime_apikey: ApiKeyValue
    from_file_apikey: ApiKeyValue
    from_file_options_api_key: ApiKeyValue

    def __init__(self):
        self.runtime_apikey = ApiKeyValue("runtime", False, ApiKeyType.runtime)
        self.from_file_apikey = ApiKeyValue("fromfile", False, ApiKeyType.from_file)
        self.from_file_options_api_key = ApiKeyValue("fromfile_options", False, ApiKeyType.from_file_options)

    def set_value(self, type_: Union[str, ApiKeyType], value):
        if type_ in ["runtime", ApiKeyType.runtime]:
            self.runtime_apikey.value = value
            return
        if type_ in ["fromfile", ApiKeyType.from_file]:
            self.from_file_apikey.value = value
            return
        self.from_file_options_api_key = value


import time


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

    def no_api_msg(self):
        template = f"""
        Api Key not set yet.
        --------------------------------------------
        how to set api key?
        --------------------------------------------
        Option 1 (from console)
            $ evdspy save
        Option 2 (python console with menu)
            python> from evdspy import menu
            python> menu()
            Selection 10
            10 | SAVE API KEY TO FILE
        Option 3 (python console )
            python> from evdspy import save
            python> save()
        """
        print(template)

    def get_valid_api_key(cls, check=False):
        if cls.now_testing_is_key_is_valid:
            return cls.now_testing_is_key_is_valid
        key_objs = cls.get_api_keys()
        if not key_objs:
            if check:
                cls.no_api_msg()
                time.sleep(4)
                raise ApiKeyNotSetError("No valid API keys found")
            if config.current_mode_is_test:
                return "VALID_KEY_FOR_TEST"
            return False
        return key_objs[0].value

    @property
    def key(self):
        if config.current_mode_is_test:
            return "VALID_KEY_FOR_TEST"
        key = self.get_valid_api_key(check=True)
        return key

    @staticmethod
    def obscure(key=None):
        from evdspy.EVDSlocal.utils.utils_general import encode
        if key is None:
            key = ApikeyClass().key
        if not isinstance(key, str):
            return "..."

        strings = []
        for index, i in enumerate(str(encode(key))):
            if index < 7 or index % 3 == 0:
                strings.append("*")
            else:
                strings.append(i)
        return "".join(strings)

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
        return cls.instance.APIKEYDict.from_file_options_api_key
