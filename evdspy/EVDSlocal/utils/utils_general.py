
#### 1 ###############
import base64
import functools
import locale
# from babel.numbers import format_decimal
import pickle
import functools
import weakref
import functools
import os.path
from pathlib import Path
import sys
indent = " " * 15
ENCODING = "utf-8"
#### 2 ###############
import os
#### GLOBALS ###############
#### -- ###############
from datetime import date
today = date.today()
stoday = str(today)
import time
import os
def ls():
    print(os.popen("ls -l").read())

def decode(base64_bytes) -> str:
    if isinstance(base64_bytes, str):
        base64_bytes = str.encode(base64_bytes)
    str_bytes = base64.b64decode(base64_bytes)
    decoded = str_bytes.decode("ascii")
    return decoded
def encode(text: str) -> bytes:
    t_bytes = text.encode("ascii")
    encoded = base64.b64encode(t_bytes)
    return encoded

def replace_recursive(content: str, char: str, new_char: str):
    if char not in content:
        return content
    content = content.replace(char, new_char)
    return replace_recursive(content, char, new_char)
    
def api_key_looks_valid(key: str):
    return isinstance(key, str) and len(key) == 10
class ApiKeyErrorEnvir(BaseException):
    """ApiKeyErrorEnvir"""
def get_env_api_key(check=False):
    key = os.getenv("EVDS_API_KEY")
    if check and not api_key_looks_valid(key):
        from evdspy.EVDSlocal.utils.utils_test import get_api_key_while_testing
        api_key = get_api_key_while_testing()
        if api_key_looks_valid(api_key):
            return api_key
        raise ApiKeyErrorEnvir("ApiKeyErrorEnvir")
    return key
def do_if_callable(f):
    if callable(f):
        f()
from pathlib import Path
def URL_temizle(url: str):
    import string
    return url.translate({ord(c): None for c in string.whitespace})
def arg_acc(argv=None):
    if argv is None:
        argv = sys.argv
    obj = {}
    for index, key in enumerate(argv):
        key = str(key)
        if key.startswith("--"):
            value = None
            if len(argv) > index + 1:
                value = argv[index + 1]
            key = key[2:]
            obj.update({key: value})
    return obj
def get_current_dir():
    return Path(__file__).parent
def get_current_dir2(pat):
    d = pat.absolute()
    return d
def delay(s: int, f1=None, f2=None):
    do_if_callable(f1)
    time.sleep(s)
    do_if_callable(f2)
def ro(amount: float):
    return round(amount)
def bound(f, *args):
    return functools.partial(f, *args)
def create_directory(adres: str) -> None:
    import os
    if not os.path.isdir(adres):
        os.makedirs(adres)
def get_api_key_from_file(file_name):
    lines = False
    file_name_path = Path(file_name)
    if not file_name_path.is_file():
        return False
    with open(file_name, encoding=ENCODING) as file:
        lines = file.readlines()
    if lines is False:
        return False
    return str(lines[0]).strip()  # .split(":")[1]
def global_var_api_key():
    import os
    return "This version does not read global EVDS"
    API_KEY_NAME = "EVDS_API_KEY"
    return os.getenv(API_KEY_NAME)
def get_proxy_from_file(file_name):
    lines = False
    if not file_name:
        return False
    file_name_path = Path(file_name)
    if not file_name_path.is_file():
        return False
    with open(file_name_path, encoding=ENCODING) as file:
        lines = file.readlines()
    if lines is False:
        return False
    return lines[0]  # ":".join(lines[0].split(":")[1:])
def reducer(liste):
    functools.reduce(lambda a, b: a + b, liste)
def reducer_prop(liste, prop="guncel_tutar"):
    # print(liste ,prop , "---" )
    return functools.reduce(lambda a, b: a + b,
                            [getattr(item, prop) for item in liste])
def f2(amount):
    return '{:7,.2f}'.format(amount)
def f0(amount):
    return '{:7,.0f}'.format(amount)
def get_random_hash(num=5):
    import random
    import string
    letters = string.ascii_letters
    randomF = ''.join(random.choice(letters) for i in range(num))
    return randomF
