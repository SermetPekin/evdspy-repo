# ...........................................................................................
from evdspy import setup
from evdspy.EVDSlocal.components.excel_class import replace_all
from evdspy.EVDSlocal.index_requests.get_series_indexes_utils import (
    default_start_date_fnc,
    default_end_date_fnc, correct_types,
)
from evdspy.EVDSlocal.utils.utils_test import get_api_key_while_testing, ApiClassWhileTesting
from evdspy.EVDSlocal.index_requests.index_util_funcs import json_to_df, make_df_float
from evdspy.EVDSlocal.requests_.real_requests import *
from evdspy.EVDSlocal.utils.github_actions import PytestTesting, GithubActions
from evdspy.EVDSlocal.index_requests.get_series_indexes_utils import (
    freq_enum,
    Formulas,
    AggregationType
)
# ...........................................................................................
from requests import HTTPError
import requests
from dataclasses import dataclass
from typing import Union, Callable
import pandas as pd
import json
from abc import ABC


# ....................................................................... ProxyManager
@dataclass
class ProxyManager:
    proxy: Optional[str] = None
    proxies: Optional[dict[Any, Any]] = None

    def get_proxies(self) -> Optional[dict[Any, Any]]:
        if self.proxies is None:
            if self.proxy is None:
                proxies = None
            else:
                proxies = self.get_proxies_helper()
        else:
            proxies = self.proxies
        return proxies

    def get_proxies_helper(self) -> Optional[dict[Any, Any]]:
        if self.proxy is None:
            return None
        proxy = self.proxy
        proxies = {
            'http': proxy,
            'https': proxy,
        }
        return proxies


# ....................................................................... Serialize
class Serialize(ABC):
    """To check whether two Config Requests are perfect substitutes """

    def serialize(self):
        return json.dumps(
            self,
            default=lambda o: o.__dict__,
            sort_keys=True,
            indent=4)

    @property
    def hash(self) -> str:
        import hashlib
        return str(int(hashlib.sha256(self.serialize().encode('utf-8')).hexdigest(), 16) % 10 ** 8)

    def __eq__(self, other):
        return self.hash == other.hash


# ................................................................. UserRequestUtils
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


# ....................................................................... RequestConfig
# typings .......................................................... typings

T_str_int_None = Union[str, int, None]
T_str_tuple_None = Union[str, tuple[str], None]
T_tuple_str_int_None = Union[str, int, tuple[str], tuple[int], None]
T_maybeDf = Union[pd.DataFrame, bool, None]


# ................................................................... RequestConfig
@dataclass
class RequestConfig(Serialize):
    index: Union[str, tuple[str, ...], list[str, ...]]
    start_date: str = default_start_date_fnc()
    end_date: str = default_end_date_fnc()
    frequency: T_str_int_None = None
    formulas: T_tuple_str_int_None = None
    aggregation: T_str_tuple_None = None
    cache: bool = False
    cache_name: str = ""
    initial_index = None
    # series_url_instance: SeriesUrlClass = SeriesUrlClass()
    """
    Represents a user request for fetching data series from a specified source.
    This class encapsulates the details necessary to construct and execute a data retrieval request,
    handling various configurations like date ranges, frequency, and data aggregation types. It
    also manages proxy settings and caching mechanisms to optimize data retrieval operations.
    Attributes:
        index (Union[str, Tuple[str]]): The identifier(s) for the data series to fetch.
        start_date (str): The start date for the data retrieval in 'DD-MM-YYYY' format.
        end_date (str): The end date for the data retrieval in 'DD-MM-YYYY' format.
        frequency (Union[str, int, None]): The frequency at which data should be retrieved.
        formulas (Union[str, int, Tuple[str, int], None]): The calculation types to apply to the data.
        aggregation (Union[str, Tuple[str], None]): The aggregation methods to apply to the data.
        cache (bool): Enables or disables caching of the request results.
        cache_name (str): The name under which to store the cached results, if caching is enabled.
        series_url_instance (SeriesUrlClass): An instance of SeriesUrlClass to handle URL creation.
    Methods:
        __post_init__: Initializes further attributes and performs checks after the basic initialization.
    Raises:
        ValueError: If the index is in an invalid format or necessary attributes are missing.
    """

    def check_type(self):
        if UserRequestUtils.looks_like_datagroup(self.initial_index):
            return "datagroup"
        return "series"

    def __post_init__(self):
        self.initial_index = self.index
        self.correct_index()
        self.correct_formulas_aggr()
        self.check()

    def upper_index(self) -> None:
        def upper(string: str) -> str:
            if UserRequestUtils.looks_like_datagroup(self.initial_index):
                return string
            return string.upper()

        self.index = tuple(map(upper, self.index))

    def clean(self) -> None:
        self.index = tuple(map(UserRequestUtils.clean_chars, self.index))

    def correct_index(self):
        if "\n" in self.index or "\t" in self.index:
            self.index = self.template_to_tuple(self.index)
        self.index = tuple([self.index]) if not isinstance(self.index, (tuple, list,)) else self.index
        self.clean()
        self.upper_index()
        self.check_index()

    def correct_formulas_aggr(self):
        self.formulas = self.correct_type_to_tuple(self.formulas)
        self.aggregation = self.correct_type_to_tuple(self.aggregation)

    def correct_type_to_tuple(self, value: any) -> Optional[tuple]:
        if value is None:
            return None
        if isinstance(value, (list, tuple)):
            if len(value) == len(self.index):
                return value
        if isinstance(value, (str,)):
            return tuple(value for _ in self.index)
        return tuple(value[0] for _ in self.index)

    @staticmethod
    def template_to_tuple(index: str) -> tuple:
        def clean(string: str):
            return string.split("#")[0].strip() if len(string.split("#")) > 0 else None

        index = replace_all(index, "\t", "\n")
        index_tuple = index.splitlines()
        t = tuple(clean(x) for x in index_tuple)
        return tuple(x for x in t if x is not None and len(x) > 3)

    def check_index(self) -> None:
        if isinstance(self.index, (int, float,)):
            raise ValueError("index must be a string ot tuple of string ")

    def freq_str(self) -> str:
        if self.frequency is None:
            return ""
        if isinstance(self.frequency, int):
            return f"&frequency={self.frequency}"
        return freq_enum(self.frequency)

    def agr_form_type_to_str(self, value: Optional[tuple], part_name="aggregationTypes"):
        if value is None:
            return ""
        value = tuple(map(str, value))
        string = "-".join(value)
        return f"&{part_name}=" + string

    def aggregation_type_to_str(self) -> str:
        self.aggregation = correct_types(self.aggregation, enum_class=AggregationType)
        return self.agr_form_type_to_str(self.aggregation, "aggregationTypes")

    def formulas_to_str(self) -> str:
        self.formulas = correct_types(self.formulas, enum_class=Formulas)
        return self.agr_form_type_to_str(self.formulas, "formulas")

    def check(self) -> None:
        if self.formulas is not None:
            assert len(self.formulas) == len(self.index)
        if self.aggregation is not None:
            assert len(self.aggregation) == len(self.index)
        if self.frequency is not None:
            assert isinstance(self.frequency, (int, str,))

    def create_series_part(self) -> str:
        indexes = self.index
        if isinstance(indexes, str):
            indexes = tuple([indexes])
        return "-".join(indexes)


# ....................................................................... UrlSeries
class UrlSeries:
    @property
    def domain(self) -> str:
        return "https://evds2.tcmb.gov.tr/service/evds"

    @property
    def alias(self):
        return "series="


# ....................................................................... UrlDataGroup
class UrlDataGroup(UrlSeries):
    @property
    def alias(self):
        return "datagroup="


# ....................................................................... UrlBuilder
class UrlBuilder:
    def __init__(self,
                 config: RequestConfig,
                 url_type=None) -> None:
        self.config = config
        self.series_part = self.config.create_series_part()
        if not url_type:
            self.get_url_type()
        self.alias = self.url_type.alias

    def get_url_type(self):
        url_type = UrlSeries()
        if self.config.check_type() == "datagroup":
            url_type = UrlDataGroup()
        self.url_type = url_type

    def create_url_for_series(cls) -> str:
        domain = cls.domain
        return f"{domain}/{cls.alias}{cls.series_part}&startDate={cls.config.start_date}&endDate={cls.config.end_date}&type=json"

    @property
    def domain(self) -> str:
        return self.url_type.domain

    @property
    def basic_url(self) -> str:
        config = self.config
        return f"{self.domain}/{self.alias}{self.series_part}&startDate={config.start_date}&endDate={config.end_date}&type=json"

    @property
    def url(self) -> str:
        config = self.config
        if config.frequency is None and config.aggregation is None and config.formulas is None:
            return self.basic_url
        """ config parts """
        formulas_str = config.formulas_to_str()
        aggregation_type_str = config.aggregation_type_to_str()
        freq_string = config.freq_str()
        """..."""
        parts = (
            f"{self.domain}/{self.alias}{self.series_part}{freq_string}{formulas_str}{aggregation_type_str}",
            f"startDate={config.start_date}",
            f"endDate={config.end_date}",
            "type=json"
        )
        return "&".join(parts)


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


def test_cache_or_raw_fnc(capsys):
    with capsys.disabled():
        setup()
        fnc = lambda x: x ** 2
        f = cache_or_raw_fnc(fnc, True)
        f2 = cache_or_raw_fnc(fnc, False)
        assert f(3) == 9
        assert f2(3) == 9
        assert id(f2) != id(f)


# ....................................................................... ApiRequester
class ApiRequester:
    def __init__(self, url_builder: UrlBuilder, proxy_manager: ProxyManager):
        self.url_builder = url_builder
        self.proxy_manager = proxy_manager
        self.proxies = self.proxy_manager.get_proxies()
        self.url = self.url_builder.url
        self.response = None

    def get(self):
        return self.request()

    def __call__(self, *args, **kwargs):
        return self.get()

    def dry_request(self) -> RequestConfig:
        api_key = self.get_api_key(check=False)
        print(f"""
---------------------------------
    [debug mode is turned on]
        api_key = {self.obscure(api_key)}
        proxies = {self.proxies}
        url  = {self.url}
    ! request was not made because debug mode is turned on
    in order to make the request run get_series(... , debug = False )
---------------------------------
""")
        return self.url_builder.config

    def is_response_ok(self, response):
        return isinstance(response, requests.Response) \
            and response.status_code == 200

    @staticmethod
    def obscure(string: str):
        return ApikeyClass().obscure(string)


    def get_api_key(self, check=True) -> str:
        if PytestTesting().is_testing() or GithubActions().is_testing():
            api_key = self.get_api_key_while_testing()
        else:
            api_key = ApikeyClass().get_valid_api_key(check=check)
        return api_key

    def get_api_key_while_testing(self):
        return ApiClassWhileTesting()()

    def request(self) -> Any:
        api_key = self.get_api_key()
        if api_key is False:
            if GithubActions().is_testing():
                return self.dry_request()
            if PytestTesting().is_testing():
                raise NotImplementedError
        proxies = self.proxy_manager.get_proxies()

        def local_request(url: str) -> requests.Response:
            requester = RealRequestWithParam(url,
                                             proxies=proxies,
                                             api_key=api_key)
            return requester.request()

        request_func = cache_or_raw_fnc(local_request,
                                        cache=self.url_builder.config.cache)
        response = False
        try:
            response = request_func(self.url)
        except Exception as exc:
            traceback.print_exc()
        self.response = response
        if not self.is_response_ok(response):
            return False
            # raise HTTPError(response=response)
        return response.json()

    def is_ok(self) -> bool:
        response = self.response
        ok = isinstance(response, requests.Response) and response.status_code == 200
        if not ok:
            self.dry_request()
            raise ValueError("request Not Ok")
        else:
            print("<data is here>")
        return ok


import traceback


# ....................................................................... DataProcessor
class DataProcessor:
    def __init__(self, data: Any):
        self.data = data

    def process_to_dataframe(self) -> T_maybeDf:
        if self.data is False:
            return False
        try:
            df = json_to_df(self.data)
        except Exception as e:
            print(e)
            traceback.print_exc()
            return None
        if isinstance(df, pd.DataFrame):
            df = make_df_float(df)
        return df

    def __call__(self, *args, **kwargs) -> T_maybeDf:
        return self.process_to_dataframe()


def test_DataProcessor(capsys):
    with capsys.disabled():
        d = DataProcessor(False)
        print(d)
