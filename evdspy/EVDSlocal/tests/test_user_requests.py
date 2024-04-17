from pathlib import Path
import pandas as pd
from evdspy.EVDSlocal.index_requests.get_series_indexes import default_start_date_fnc, \
    default_end_date_fnc, get_series
from evdspy.EVDSlocal.utils.github_actions import GithubActions
from evdspy.EVDSlocal.utils.utils_general import get_env_api_key
from evdspy.EVDSlocal.utils.utils_test import get_api_key_while_testing
from evdspy.EVDSlocal.index_requests.get_series_indexes_utils import Frequency, freq_enum, Formulas, AggregationType, \
    correct_types
# from evdspy.EVDSlocal.index_requests.user_requests import
from evdspy.EVDSlocal.config.apikey_class import ApikeyClass
from evdspy.EVDSlocal.index_requests.get_series_indexes_utils import default_start_date_fnc, default_end_date_fnc
from evdspy.EVDSlocal.index_requests.user_requests import ProxyManager, UrlBuilder, UrlSeries, ApiRequester, \
    DataProcessor, RequestConfig


def test_get_series_bridge(capsys):
    with capsys.disabled():
        df = get_series("bie_gsyhgycf", cache=False, api_key=get_env_api_key(check=True))
        assert isinstance(df, pd.DataFrame)


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
        df = get_series(template, debug=False, cache=False, api_key=get_env_api_key(check=True))
        assert isinstance(df, pd.DataFrame)


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
        if is_testing():
            return
        a1 = get_series(balance_of_pay1, debug=False)
        print(a1)
        assert isinstance(a1, pd.DataFrame)


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


def get_api_key():
    import os
    return os.getenv("EVDS_API_KEY")


# assert isinstance(get_api_key(), str) and len(get_api_key()) == 10
def key_valid():
    return isinstance(get_api_key(), str) and len(get_api_key()) == 10


def is_testing():
    return GithubActions().is_testing() and not key_valid()


def test_get_series2(capsys):
    with capsys.disabled():
        if is_testing():
            return
        # setup()
        # print(Path().absolute())
        df = get_series("TP.ODEMGZS.BDTTOPLAM",
                        cache=False)
        assert isinstance(df, pd.DataFrame)


def test_get_df_datagroup(capsys):
    if not GithubActions().is_testing():
        return
    from evdspy.main import get_df_datagroup
    df = get_df_datagroup(
        datagroup="bie_gsyhgycf",
        start_date="01-01-1998",
        end_date="01-01-2030",
    )
    print(df)


def test_get_api_key_while_testing(capsys):
    with capsys.disabled():
        if GithubActions().is_testing():
            return

        a = get_api_key_while_testing()
        assert len(a) > 5 and 'lg' in a


def test_get_series(capsys):
    if is_testing():
        return
    with capsys.disabled():
        if is_testing():
            return
        index = 'TP.YSSK.A1'
        start_date = "01-01-2000"
        end_date = "01-01-2100"
        cache = True
        # user_req = UserRequest(index, start_date, end_date)
        df = get_series(index, start_date, end_date, cache)
        print(df)


# from evdspy.EVDSlocal.index_requests.get_series_indexes import Formulas, correct_types, AggregationType
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
# def test_UserRequest(capsys):
#     with capsys.disabled():
#         print("\n")
#         ur = RequestConfig("TP.ODEMGZS.BDTTOPLAM")
#         assert ur.url == "https://evds2.tcmb.gov.tr/service/evds/series=TP.ODEMGZS.BDTTOPLAM&startDate=01-01-2000&endDate=01-01-2100&type=json"
#         ur = RequestConfig(("Aaa", "Bbb",),
#                          start_date=default_start_date_fnc(),
#                          end_date=default_end_date_fnc(),
#                          aggregation=("avg",))
#         assert ur.url == "https://evds2.tcmb.gov.tr/service/evds/series=Aaa-Bbb&aggregationTypes=avg-avg&startDate=01-01-2000&endDate=01-01-2100&type=json"
#         ur = RequestConfig(("Aaa", "Bbb",),
#                          start_date=default_start_date_fnc(),
#                          end_date=default_end_date_fnc(),
#                          aggregation=("avg",),
#                          formulas="level")
#         assert ur.url == "https://evds2.tcmb.gov.tr/service/evds/series=Aaa-Bbb&formulas=0-0&aggregationTypes=avg-avg&startDate=01-01-2000&endDate=01-01-2100&type=json"
#         ur = RequestConfig(("Aaa", "Bbb",),
#                          frequency=3,
#                          start_date=default_start_date_fnc(),
#                          end_date=default_end_date_fnc(),
#                          aggregation=("avg",),
#                          formulas="level")
#         print(ur.url)
#         assert ur.url == "https://evds2.tcmb.gov.tr/service/evds/series=Aaa-Bbb&frequency=3&formulas=0-0&aggregationTypes=avg-avg&startDate=01-01-2000&endDate=01-01-2100&type=json"
