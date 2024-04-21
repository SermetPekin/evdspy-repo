# ................................................................. UserRequestUtils
# ...........................................................................................
from evdspy import setup



from evdspy.EVDSlocal.requests_.real_requests import *
# ...........................................................................................
from typing import Union, Callable



class UserRequestUtils:
    @staticmethod
    def looks_like_datagroup(string: Any):
        if not isinstance(string, str):
            return False
        return 'bie_' in string

    @staticmethod
    def clean_chars(string: str):
        import re
        if UserRequestUtils().looks_like_datagroup(string):
            string = re.sub('[^0-9a-zA-Z._]+', '', string)
            return string
        string = string.replace("_", ".")
        string = re.sub('[^0-9a-zA-Z.]+', '', string)
        return string


def test_clean_chars(capsys):
    with capsys.disabled():
        assert UserRequestUtils.clean_chars("AAA_BBB?*-()$? ") == "AAA.BBB"
        assert UserRequestUtils.clean_chars("AAA..._BBB?*-()$? ") == "AAA....BBB"
        assert UserRequestUtils.clean_chars("bie_BBB?*-()$? ") == "bie_BBB"


def test_cache_or_raw_fnc(capsys):
    with capsys.disabled():
        setup()
        fnc = lambda x: x ** 2
        f = cache_or_raw_fnc(fnc, True)
        f2 = cache_or_raw_fnc(fnc, False)
        assert f(3) == 9
        assert f2(3) == 9
        assert id(f2) != id(f)


# ..................................................................................

def create_cache_version(fnc: Callable):
    @MyCache().cache
    def fnc_cache(*args, **kw):
        return fnc(*args, **kw)

    return fnc_cache


def cache_or_raw_fnc(fnc, cache=False):
    if not cache:
        return fnc
    return create_cache_version(fnc)
