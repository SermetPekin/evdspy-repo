from pathlib import Path
from typing import Any
import pandas as pd
from evdspy.EVDSlocal.index_requests.get_series_indexes import default_start_date_fnc, \
    default_end_date_fnc, get_series
from evdspy.EVDSlocal.utils.github_actions import GithubActions
from evdspy.EVDSlocal.utils.utils_general import get_env_api_key
from evdspy.EVDSlocal.utils.utils_test import get_api_key_while_testing, ApiClassWhileTesting, get_api_key_file, \
    skip_if_gthub, skip_if_not_keyvalid, is_df
from evdspy.EVDSlocal.index_requests.get_series_indexes_utils import Frequency, freq_enum, Formulas, AggregationType, \
    correct_types
# from evdspy.EVDSlocal.index_requests.user_requests import
from evdspy.EVDSlocal.config.apikey_class import ApikeyClass
from evdspy.EVDSlocal.index_requests.get_series_indexes_utils import default_start_date_fnc, default_end_date_fnc
from evdspy.EVDSlocal.index_requests.user_requests import (ProxyManager, UrlBuilder, UrlSeries,
                                                           ApiRequester, DataProcessor, RequestConfig)

# from evdspy.EVDSlocal.index_requests.get_series_indexes_utils import *

try:
    import pytest
except ImportError:
    pass


@skip_if_gthub
def test_get_api_key_file(capsys):
    with capsys.disabled():
        api_key_file = get_api_key_file(deep=8)
        print(api_key_file.absolute())
        assert api_key_file is not None


@skip_if_gthub
def test_ApiClassWhileTesting(capsys):
    with capsys.disabled():
        api_key = ApiClassWhileTesting().key
        # print(ApikeyClass().obscure(api_key))
        print(Path('').absolute())


@skip_if_not_keyvalid
@skip_if_gthub
def test_get_series_bridge(capsys):
    with capsys.disabled():
        df = get_series("bie_gsyhgycf",
                        cache=False,
                        api_key=get_env_api_key(check=True))
        assert is_df(df)


@skip_if_not_keyvalid
def test_get_diff_series(capsys):
    with capsys.disabled():
        template = """TP_GSYIH01_GY_CF
        TP_GSYIH02_GY_CF
        TP_GSYIH03_GY_CF
        TP_GSYIH04_GY_CF
        TP_GSYIH05_GY_CF
        TP_GSYIH06_GY_CF
        TP_GSYIH07_GY_CF
        TP_GSYIH08_GY_CF
        TP_GSYIH09_GY_CF
        TP_GSYIH10_GY_CF
        TP_GSYIH11_GY_CF
        TP_GSYIH14_GY_CF
        TP_GSYIH15_GY_CF
        TP_GSYIH16_GY_CF
        """
        df = get_series(template, debug=False, cache=False,
                        api_key=get_env_api_key(check=True))
        assert is_df(df)


# @skip_if_not_keyvalid
def test_template_series(capsys):
    with capsys.disabled():
        balance_of_pay1 = "TP.ODEMGZS.BDTTOPLAM", "TP.ODEMGZS.ABD"
        balance_of_pay2 = """
        TP.ODEMGZS.BDTTOPLAM #
        TP.ODEMGZS.ABD #
        """
        a1 = get_series(balance_of_pay1, debug=True)
        a2 = get_series(balance_of_pay2, debug=True)
        print(a1.hash, a2.hash)
        assert a1 == a2


@skip_if_not_keyvalid
def test_a(capsys):
    with capsys.disabled():
        balance_of_pay1 = "TP.ODEMGZS.BDTTOPLAM", "TP.ODEMGZS.ABD"
        balance_of_pay2 = """
        TP.ODEMGZS.BDTTOPLAM #
        TP.ODEMGZS.ABD #
        """
        a1 = get_series(balance_of_pay1, debug=True)
        a2 = get_series(balance_of_pay2, debug=True)
        assert a1 == a2
        print(a1)

        a1 = get_series(balance_of_pay1, debug=False)
        print(a1)
        assert is_df(a1)


def test_template_series2(capsys):
    with capsys.disabled():
        balance_of_pay1 = "TP.ODEMGZS.BDTTOPLAM", "TP.ODEMGZS.ABD"
        balance_of_pay2 = """
        TP.ODEMGZS.BDTTOPLAM #
        TP.ODEMGZS.ABD #
        """
        a1 = get_series(balance_of_pay1, aggregation="avg", debug=True)
        a2 = get_series(balance_of_pay2, aggregation=("avg", "avg"), debug=True)
        print(a1.hash, a2.hash)
        assert a1 == a2


# @skip_if_not_keyvalid

def test_template_series3(capsys):
    with capsys.disabled():
        balance_of_pay1 = "TP.ODEMGZS.BDTTOPLAM", "TP.ODEMGZS.ABD"
        balance_of_pay2 = """
        TP.ODEMGZS.BDTTOPLAM #
        TP.ODEMGZS.ABD #
        """
        a1 = get_series(balance_of_pay1, formulas="level", debug=True)
        a2 = get_series(balance_of_pay2, formulas=(0, 0), debug=True)
        print(a1.hash, a2.hash)
        assert a1 == a2


def test_freq(capsys):
    f = Frequency.annually
    with capsys.disabled():
        assert f() == "&frequency=8"
        print("\n")
        print(f())
        g = freq_enum("daily")
        assert g == "&frequency=1"
        assert freq_enum("daily") == "&frequency=1"
        assert freq_enum("monthly") == "&frequency=5"
        assert freq_enum("annual") == "&frequency=8"
        assert freq_enum(3) == "&frequency=3"
        assert freq_enum(1) == "&frequency=1"


def test_pickles():
    import os
    os.makedirs("pickles", exist_ok=True)


# def is_testing():
#     return GithubActions().is_testing() and not key_valid()

@skip_if_not_keyvalid
def test_get_series2(capsys):
    with capsys.disabled():
        df = get_series("TP.ODEMGZS.BDTTOPLAM",
                        cache=False)
        assert isinstance(df, pd.DataFrame)


# def test_get_df_datagroup(capsys):
#     # if not GithubActions().is_testing():
#     #     return
#     from evdspy.main import get_df_datagroup
#     with capsys.disabled():
#         df = get_df_datagroup(
#             datagroup="bie_gsyhgycf",
#             start_date="01-01-1998",
#             end_date="01-01-2030",
#         )
#         print(df)
import os


def test_get_api_key_while_testing(capsys):
    with capsys.disabled():
        a = ApiClassWhileTesting().key
        assert len(a) > 5 and 'lg' in a


@skip_if_not_keyvalid
def test_get_series(capsys):
    with capsys.disabled():
        index = 'TP.YSSK.A1'
        start_date = "01-01-2000"
        end_date = "01-01-2100"
        cache = True
        df = get_series(index, start_date, end_date, cache, api_key=ApiClassWhileTesting()())
        print(df)
        assert is_df(df)


# from evdspy.EVDSlocal.index_requests.get_series_indexes import Formulas, correct_types, AggregationType
# @skip_if_not_keyvalid
def test_aggr_types(capsys):
    balance_of_pay1 = "TP.ODEMGZS.BDTTOPLAM", "TP.ODEMGZS.ABD"
    balance_of_pay2 = """
    TP.ODEMGZS.BDTTOPLAM #
    TP.ODEMGZS.ABD #
    """
    cache = True
    with capsys.disabled():
        u1 = RequestConfig(balance_of_pay1,
                           frequency="weekly",
                           start_date=default_start_date_fnc(),
                           end_date=default_end_date_fnc(),
                           aggregation=("avg",),
                           # proxy="http://127.0.0.1:8000",
                           # proxies={"http": "http://127.0.0.1:8000"},
                           cache=cache,
                           )
        u2 = RequestConfig(balance_of_pay2,
                           frequency="weekly",
                           start_date=default_start_date_fnc(),
                           end_date=default_end_date_fnc(),
                           aggregation=("avg",),
                           # proxy="http://127.0.0.1:8000",
                           # proxies={"http": "http://127.0.0.1:8000"},
                           cache=cache,
                           )
        assert u1 == u2


def test_correct(capsys):
    with capsys.disabled():
        assert hasattr(Formulas, "from_str")
        assert Formulas.level.value == 0
        assert Formulas.from_str("level").value == 0
        assert correct_types("level", Formulas) == 0
        assert correct_types(("level", "level",), enum_class=Formulas) == (0, 0,)


def test_correct2(capsys):
    with capsys.disabled():
        assert correct_types("avg", AggregationType) == "avg"
        assert correct_types(("avg", "min",), AggregationType) == ("avg", "min",)


@skip_if_not_keyvalid
def test_mixedcase_get_series(capsys):
    index = """
    tp.sekbil1122.GENEL
    tp.sekbil1122.A
    tp.sekbil1122.01
    tp.sekbil1122.02
    TP.SEKbil1122.03
    TP.sekBIL1122.B
    TP.SEKBIL1122.05
    TP.SEKBIL1122.07
    TP.sekbIL1122.08
    TP.SEKBIL1122.09
    TP.SEKBIL1122.C
    """
    with capsys.disabled():
        df = get_series(index)
        assert is_df(df)


@skip_if_not_keyvalid
def test_gets_upper(capsys):
    with capsys.disabled():
        template = """TP_GSYIH01_GY_CF
                tp_gsyih02_gy_cf
                tp_gsyih03_gy_cf
                tp_gsyih04_gy_cf
                tp_gsyih05_GY_CF
                TP_GSYIH06_GY_CF
                TP_GSYIH07_GY_CF
                TP_GSYIH08_GY_CF
                TP_GSYIH09_GY_CF
                TP_GSYIH10_GY_CF
                TP_GSYIH11_GY_CF
                TP_GSYIH14_GY_CF
                TP_GSYIH15_GY_CF
                TP_GSYIH16_GY_CF
        """
        df = get_series(template)
        assert is_df(df)


# @skip_if_not_keyvalid
def test_multi(capsys):
    template = """
bie_sekbil1122
bie_sekbil1001
bie_sekbil3111
bie_sekbil3001
bie_sekbil3051
    """
    names = tuple(x for x in template.splitlines() if x.strip())
    print(names)
    dfs = tuple(map(get_series, names))
    assert all(map(lambda x: is_df(x), dfs))
    tuple(map(lambda x: print(x.shape), dfs))


@skip_if_not_keyvalid
def test_get_series_b(capsys):
    index = """
    TP.OSUVBG01 # some comments
TP.OSUVBG02 # ...
TP.OSUVBG03
    TP.OSUVBG04
    TP.OSUVBG05
    TP.OSUVBG06 #
    TP.OSUVBG07  # some comments
    TP.OSUVBG08 #
    TP.OSUVBG09   # some more comments
 TP.OSUVBG10
TP.OSUVBG11
TP.OSUVBG12
TP.OSUVBG13
TP.OSUVBG14
    """
    with capsys.disabled():
        df = get_series(index)
        assert is_df(df)
