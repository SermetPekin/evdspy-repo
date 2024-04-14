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
