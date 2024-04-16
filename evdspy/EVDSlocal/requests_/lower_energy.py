
import functools
import random
import time
# --------------------------------------------------------------------------------------
if __name__ != "__main__":
    from evdspy.EVDSlocal.common.files import WriteBytes, ReadBytes, WriteBytesAdd
    from evdspy.EVDSlocal.config.config import ConfigBase, config
    from evdspy.EVDSlocal.manual_requests.prepare import basic_for_test, PrepareUrl
else:
    def WriteBytes(file_name: str, content_bytes: bytes):
        with open(file_name, 'wb+') as f:
            f.write(content_bytes)
    def WriteBytesAdd(file_name: str, content_bytes: bytes):
        with open(file_name, 'ab') as f:
            f.write(content_bytes)
    def ReadBytes(file_name: str):
        with open(file_name, "rb") as f:
            return f.read()
# --------------------------------------------------------------------------------------
import base64
import hashlib
import os
from pathlib import Path
from dataclasses import dataclass
from typing import List, Tuple
from typing import Union, Callable
from evdspy.EVDSlocal.initial.start_options import default_arch_folder_name, default_arch_file_name
if config.current_mode_is_test:
    default_arch_folder_name = f"--Test--/{default_arch_folder_name}"
item_sep = "\n"
item_sep_bytes = bytes(item_sep, encoding="utf8")
def get_pepper():
    """ trying to get extra sec by getting info that will be different for all users
        but will not change often.
        If it changes it will just result a new request until it changes
        again though, so not a big burden.
    """
    pepper = "The quick brown fox, why not"
    import os
    try:
        u = os.environ.get("USERNAME")
    except:
        u = "any_user"
    try:
        p = Path()
    except:
        p = "path"
    pepper = f"{pepper}-{u}-{p}"
    return pepper
@dataclass
class ArchFile():
    path: Union[str, Path] = ""
    file_name: Union[str, Path] = default_arch_file_name
    def __post_init__(self):
        if isinstance(self.path, str):
            self.path = Path.cwd() / default_arch_folder_name
        self.file_name = self.path / default_arch_file_name
arch = ArchFile()
def create_folder_if_not_exist():
    if not arch.path.is_dir():
        os.makedirs(arch.path)
def setup_is_ok():
    return ArchFile().file_name.is_file()
def one_way(x, num=27):
    x = x.encode("utf-8")
    hasher = hashlib.sha1(x)
    return base64.urlsafe_b64encode(hasher.digest()[:num])
def with_pepper(x: str):
    pepper = get_pepper()
    return f"{pepper}{x}"
def name_format(api_key: str, status_code: Union[bool, int]) -> str:
    status_code = convert_status_code(status_code)
    return f"{api_key}-{get_pepper()}-{status_code}"
shuffle = True
def shuffle_content(old_content: bytes, bytes_api_key_pepper) -> bytes:
    old_list: List[bytes] = old_content.split(item_sep_bytes)
    new_list: List[bytes] = old_list + [bytes_api_key_pepper]
    content: bytes = functools.reduce(lambda x, p: x + p + item_sep_bytes, new_list)
    return content
def add_checked_hashes(api_key: str, status_code: Union[bool, int]):
    status_code: int = convert_status_code(status_code)
    create_folder_if_not_exist()
    bytes_api_key_pepper = one_way(name_format(api_key, status_code))
    assert isinstance(status_code, bool) is False, "something w"
    if shuffle:
        if not setup_is_ok():
            old_content: bytes = bytes("start", encoding="utf-8")
            new_content = bytes_api_key_pepper + item_sep_bytes
        else:
            old_content: bytes = ReadBytes(str(arch.file_name))
            new_content: bytes = shuffle_content(old_content, bytes_api_key_pepper + item_sep_bytes)
        WriteBytes(str(arch.file_name), new_content)
    else:
        WriteBytesAdd(str(arch.file_name), bytes_api_key_pepper + item_sep_bytes)
def get_list_of_cache():
    content_byte: bytes = ReadBytes(arch.file_name)
    item_list: List[bytes] = content_byte.split(item_sep_bytes)
    item_list_str: Tuple[str] = tuple(map(str, item_list))
    return item_list_str
def convert_status_code(status_code_new: Union[bool, int]) -> int:
    if isinstance(status_code_new, int) and not isinstance(status_code_new, bool):
        return status_code_new
    obj = {True: 200, False: 500}
    status_code_new = obj[status_code_new]
    return status_code_new
def check_api_key_hashes_opt(api_key, status_code: Union[bool, int]):
    status_code: int = convert_status_code(status_code)
    new_hash = one_way(name_format(api_key, status_code))
    return str(new_hash) in get_list_of_cache()
def populate_first_rand():
    if not setup_is_ok():
        create_folder_if_not_exist()
    for item in range(100):
        status_code = 500  # random.choice((200, 500))
        x_tuple = (f"test-{item}", status_code)
        # add_checked_hashes(f"test-{item}", status_code)
        add_checked_hashes(*x_tuple)
@dataclass
class Checked:
    never_checked: bool
    checked_before_and_passed: bool
    checked_before_and_failed: bool
def check_if_api_key_was_checked_before(api_key: str) -> Checked:
    """
    Every time user gives an api key to save
        we need to check if it is working.
        In earlier versions we were checking with
        a new request each time without caching.
        This version this will be a better solution which  attempts to optimize
        min request and min collision of one way hashing.
            Functions of this file are only for minimizing new request on setting api key.
            @params
                api_key : str
    """
    checked_before_and_passed = check_api_key_hashes_opt(api_key, 200)
    checked_before_and_failed = check_api_key_hashes_opt(api_key, 500)
    never_checked = not any((checked_before_and_passed, checked_before_and_failed))
    return Checked(never_checked, checked_before_and_passed, checked_before_and_failed)
testing = False
test_apikeys_success = ("s1", "s2", "s3", "s4", 'testApiKeyMock')
test_apikeys_fails = ("f1", "f2")
common_test_words = ("test", "t", "api", "key", "apikey", "key", "tested")
from ..common.colors import *
def apikey_works(api_key, check_func_request: Callable = basic_for_test, testing_=False):
    result = apikey_works_helper(**locals())
    msg_success = "Your api key was tested with success."
    msg_fails = "Your api key was tested with success."
    if result:
        print_with_success_style(msg_success)
    else:
        print_with_failure_style(msg_fails)
    return result
def apikey_works_helper(api_key, check_func_request: Callable = basic_for_test, testing_=False):
    if not setup_is_ok():
        populate_first_rand()
    ans: Checked = check_if_api_key_was_checked_before(api_key)
    checked_before = not ans.never_checked
    if checked_before:
        if ans.checked_before_and_passed:
            return True
        if ans.checked_before_and_failed:
            return False
        raise "something wrong lower energy"
    # check request
    """ make request """
    if testing or \
            testing_ or \
            config.current_mode_is_test or \
            api_key in test_apikeys_success or \
            api_key in test_apikeys_fails or \
            api_key in common_test_words:
        """ for testing """
        status_code_new: bool = api_key in test_apikeys_success  # random.choice((200, 500,))
        print_with_creating_style("first part ", api_key, status_code_new)
    else:
        if api_key in common_test_words:
            print_with_failure_style(f"api key does not look like a key. Returning...")
            return apikey_works_helper(api_key, testing_=True)
            # raise "cannot make a new request"
        # temp test forced
        # print("temp test forced")
        # return apikey_works_helper(api_key, testing_=True)
        print_with_updating_style("WARNING making a new request to test your Api key ")
        time.sleep(2)
        status_code_new: bool = check_func_request(api_key)
    """ add one way comp. hash to archive """
    add_checked_hashes(api_key, status_code_new)
    return status_code_new
__all__ = [
    'apikey_works'
]