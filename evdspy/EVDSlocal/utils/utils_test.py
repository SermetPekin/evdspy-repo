import os
from pathlib import Path
from typing import Optional, Any
import pandas as pd
from .github_actions import GithubActions
from ..common.files import Read
from ..config.apikey_class import ApikeyClass

"""Globals  """
EVDS_API_KEY_ENV_NAME = "EVDS_API_KEY"
try:
    import pytest
except Exception:
    pass


def get_api_key():
    import os
    return os.getenv("EVDS_API_KEY")


def key_valid():
    return isinstance(get_api_key(), str) and len(get_api_key()) == 10


def is_df(df: Any):
    return isinstance(df, pd.DataFrame)


def gth_testing():
    return GithubActions().is_testing()


reason_gth = "passing when github Actions "

skip_if_gthub = pytest.mark.skipif(
    gth_testing, reason=reason_gth
)

skip_if_not_keyvalid = pytest.mark.skipif(
    key_valid(), reason='No Api key Valid provided'
)


def get_api_env_key_name():
    return EVDS_API_KEY_ENV_NAME


# import pytest
def get_api_key_file(file_name="api_key.txt", deep=7) -> Optional[Path]:
    def get_file_deep(number):
        folder = Path(".")
        for _ in range(number):
            folder = folder / ".."
            if "pycharmprojects" not in str(folder.absolute()).lower() and  'evdspy-dev' not in str(folder.absolute()).lower() :
                """Do not go back deeper if it is not my folder"""
                return None
            file_namex = folder / file_name
            if file_namex.exists():
                return file_namex
        return None

    return get_file_deep(deep)


def test_get_api_key_file(capsys):
    if GithubActions().is_testing(): return

    with capsys.disabled():
        api_key = get_api_key_file(deep=8)
        print(api_key)


def get_api_key_while_testing():
    file_name = get_api_key_file(deep=7)
    if file_name is None:
        return False
    content = Read(file_name)
    lines = content.splitlines()
    line = tuple(line for line in lines if "evds" in line.lower() )
    api_key = line[0].split("=")[1]
    return str(api_key).strip()


class ApiClassWhileTesting():
    """ApiClassWhileTesting"""

    def __init__(self):
        self.api_key = self.get_api_key()

    def get_api_key(self):
        if GithubActions().is_testing():
            return os.getenv(get_api_env_key_name())
        return get_api_key_while_testing()

    @property
    def key(self):
        return self.api_key

    def __call__(self, *args, **kwargs):
        return self.key


def test_ApiClassWhileTesting(capsys):
    with capsys.disabled():
        api_key = ApiClassWhileTesting().key
        print(ApikeyClass().obscure(api_key))
