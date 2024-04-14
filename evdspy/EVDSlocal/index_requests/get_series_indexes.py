from requests import HTTPError
from evdspy.EVDSlocal.utils.utils_test import get_api_key_while_testing
from .index_util_funcs import json_to_df, make_df_float
from evdspy.EVDSlocal.requests_.real_requests import *
from ..utils.github_actions import PytestTesting
from ... import save_apikey

m_cache = MyCache()

from enum import Enum, auto
import typing as t
from dataclasses import dataclass
from typing import Union


def default_start_date_fnc():
    return "01-01-2000"


def default_end_date_fnc():
    return "01-01-2100"


class AggregationType(Enum):
    """
    avg : "avg"
    min : "min"
    max : "max"
    first : "first"
    last : "last"
    sum : "sum"


    """
    avg = "avg"
    min = "min"
    max = "max"
    first = "first"
    last = "last"
    sum = "sum"


class Formulas(Enum):
    """Formulas
    Level: 0
    Percentage change: 1
    Difference: 2
    Year-to-year Percent Change: 3
    Year-to-year Differences: 4
    Percentage Change Compared to End-of-Previous Year: 5
    Difference Compared to End-of-Previous Year : 6
    Moving Average: 7
    Moving Sum: 8

    """
    level = 0
    percentage_change = 1
    difference = 2
    year_to_year_percent_change = 3
    year_to_year_differences = 4
    percentage_change_compared = 5
    difference_compared = 6
    moving_average = 7
    moving_sum = 8


class Frequency(Enum):
    daily = 1
    business = 2
    weekly = 3  # Friday
    semimonthly = 4
    monthly = 5
    quarterly = 6
    semiannually = 7
    annual = 8
    annually = 8

    def __str__(self):
        return f"{self.value}"

    def __call__(self, *args, **kwargs):
        return f"&frequency={self.value}"


def freq_enum(frequency: Union[str, int]) -> str:
    def get_enum(value: str):
        obj = {
            "daily": Frequency.daily,
            "business": Frequency.business,
            "weekly": Frequency.weekly,
            "semimonthly": Frequency.semimonthly,
            "monthly": Frequency.monthly,
            "quarterly": Frequency.quarterly,
            "semiannually": Frequency.semiannually,
            "annual": Frequency.annually,
            "annually": Frequency.annually,
        }
        return obj.get(value, Frequency.daily)

    if isinstance(frequency, int):
        return f"&frequency={frequency}"
    return get_enum(frequency)()


def replaceAll(index: str, old: str, new: str):
    if old in index:
        index = index.replace(old, new)
        return replaceAll(index, old, new)
    return index


def test_replaceAll():
    assert replaceAll("aaa", "a", "b") == "bbb"
    assert "aaa".replace("a", "b") == "bbb"


@dataclass
class UserRequest:
    index: t.Union[str, tuple[str]]
    start_date: str = default_start_date_fnc()
    end_date: str = default_end_date_fnc()
    frequency: str = None
    formulas: str = None
    aggregation: str = None
    cache: bool = False
    proxy: str = None
    proxies: dict = None
    cache_name: str = ""

    def get_proxies(self):
        if self.proxies is None:
            if self.proxy is None:
                proxies = None
            else:
                proxies = self.get_proxies_helper()
        else:
            proxies = self.proxies
        return proxies

    def get_proxies_helper(self):

        if self.proxy is None:
            return None
        proxy = self.proxy
        proxies = {
            'http': proxy,
            'https': proxy,
        }
        return proxies

    def __post_init__(self):
        # print("post_init called")

        self.check_index()
        self.index = tuple([self.index]) if not isinstance(self.index, (tuple, list,)) else self.index
        # self.cache_name = f"{'_'.join(self.index)}_{self.start_date}_{self.end_date}"
        self.domain = domain_for_ind_series()
        self.series_part = create_series_part(self)
        self.formulas = self.correct_type_to_tuple(self.formulas)
        self.aggregation = self.correct_type_to_tuple(self.aggregation)
        # self.check_aggregation_type()
        # self.check_formulas()
        self.check()

    # @staticmethod
    def correct_type_to_tuple(self, value: any) -> tuple:

        if value is None:
            return None
        if isinstance(value, (list, tuple)):
            if len(value) == len(self.index):
                return value
        if isinstance(value, (str,)):
            return tuple(value for _ in self.index)

        return tuple(value[0] for _ in self.index)

    # def get_cache_name(self):
    #     return self.hash
    @property
    def hash(self):
        import hashlib
        return str(int(hashlib.sha256(self.url.encode('utf-8')).hexdigest(), 16) % 10 ** 8)

    def dry_request(self):
        api_key = self.get_api_key(check=False)
        proxies = self.get_proxies()
        print(f"""
---------------------------------
    [debug mode is turned on]
    
        api_key = {api_key}
        proxies = {proxies}
        url  = {self.url}
    ! request was not made because debug mode is turned on
    in order to make the request run get_series(... , debug = False )
    
--------------------------------- 
""")
        return self

    def __eq__(self, other):
        return self.index == other.index and \
            self.cache_name == other.cache_name \
            and self.url == other.url \
            and self.hash == other.hash

    def is_ok(self):
        df = self()
        ok = isinstance(df, pd.DataFrame)
        if not ok:
            self.dry_request()
            raise ValueError("request Not Ok")
        else:
            print("<data is here>")
            print(df.shape)
        return ok

    def is_response_ok(self, response):

        return isinstance(response, requests.Response) \
            and response.status_code == 200

    # @property
    def get_api_key(self, check=True):
        if PytestTesting().is_testing():
            api_key = get_api_key_while_testing()
        else:
            api_key = ApikeyClass().get_valid_api_key(check=check)

        return api_key

    def request(self):
        api_key = self.get_api_key()

        proxies = self.get_proxies()

        @m_cache.cache
        def local_request_w_cache(url: str) -> requests.Response:
            requester = RealRequestWithParam(url,
                                             proxies=proxies,
                                             api_key=api_key)
            return requester.request()

        def local_request(url: str) -> requests.Response:
            requester = RealRequestWithParam(url,
                                             proxies=proxies,
                                             api_key=api_key)
            return requester.request()

        req_func = local_request
        if self.cache:
            req_func = local_request_w_cache
        response = req_func(self.url)
        if not self.is_response_ok(response):
            print(response)
            raise HTTPError(response=response)
        # print(response)
        return response.json()

    def get(self):
        return self.get_data()

    def __call__(self, *args, **kwargs):
        return self.get()

    def get_data(self):
        json_content = self.request()
        df = json_to_df(json_content)
        df = make_df_float(df)
        return df

    @staticmethod
    def template_to_tuple(index: str):
        def clean(string: str):
            return string.split("#")[0].strip() if len(string.split("#")) > 0 else None

        index = replaceAll(index, "\t", "\n")
        index_tuple = index.splitlines()

        t = tuple(clean(x) for x in index_tuple)
        return tuple(x for x in t if x is not None and len(x) > 3)

    def check_index(self):
        if isinstance(self.index, (int, float,)):
            raise ValueError("index must be a string ot tuple of string ")
        if "\n" in self.index or "\t" in self.index:
            self.index = self.template_to_tuple(self.index)

    def basic_url(self):

        return f"{self.domain}/series={self.series_part}&startDate={self.start_date}&endDate={self.end_date}&type=json"

    def freq_str(self) -> str:
        if self.frequency is None:
            return ""

        if isinstance(self.frequency, int):
            return f"&frequency={self.frequency}"
        return freq_enum(self.frequency)

    def aggregation_type_to_str(self):
        if self.aggregation is None:
            return ""

        string = "-".join(self.aggregation)
        return "&aggregationTypes=" + string

    def formulas_to_str(self):
        if self.formulas is None:
            return ""
        index = tuple([self.index]) if not isinstance(self.index, (tuple, list,)) else self.index
        formulas = self.formulas if isinstance(self.formulas, (tuple, list,)) else tuple(self.formulas for _ in index)
        string = "-".join(formulas)
        return f"&formulas={string}"

    def check(self):
        if self.formulas is not None:
            assert len(self.formulas) == len(self.index)
        if self.aggregation is not None:
            assert len(self.aggregation) == len(self.index)

    @property
    def url(self):
        if self.frequency is None and self.aggregation is None:
            return self.basic_url()
        formulas_str = self.formulas_to_str()
        aggregation_type_str = self.aggregation_type_to_str()
        freq_string = self.freq_str()
        # series = TP.ODEMGZS.BDTTOPLAM
        # "https://evds2.tcmb.gov.tr/service/evds/series=TP.ODEMGZS.BDTTOPLAM-TP.ODEMGZS.ABD-TP.ODEMGZS.ARJANTIN-TP.ODEMGZS.BREZILYA-TP.ODEMGZS.KANADA-TP.ODEMGZS.KOLOMBIYA-TP.ODEMGZS.MEKSIKA-TP.ODEMGZS.SILI&startDate=01-01-2019&endDate=01-12-2030&frequency=5&aggregationTypes=avg-avg-avg-avg-avg-avg-avg-avg&formulas=0-0-0-0-0-0-0-0&type=csv"
        # &startDate=01-01-2019&endDate=01-12-2030&frequency=5&aggregationTypes=avg-avg-avg-avg-avg-avg-avg-avg&formulas=0-0-0-0-0-0-0-0&type=json"
        # &startDate=01-01-2019&endDate=01-12-2030&type=json"
        return f"{self.domain}/series={self.series_part}{freq_string}{formulas_str}{aggregation_type_str}&startDate={self.start_date}&endDate={self.end_date}&type=json"


def domain_for_ind_series():
    return "https://evds2.tcmb.gov.tr/service/evds"


def create_series_part(user_req):
    # print("create_series_part")
    indexes = user_req.index
    if isinstance(indexes, str):
        indexes = tuple([indexes])
    return "-".join(indexes)


def create_url_for_series(user_req: UserRequest) -> str:
    # print("create_url_for_series")
    domain = domain_for_ind_series()
    series_part = create_series_part(user_req)
    return f"{domain}/series={series_part}&startDate={user_req.start_date}&endDate={user_req.end_date}&type=json"


def get_series(
        index: t.Union[str, tuple[str]],
        start_date: str = default_start_date_fnc(),
        end_date: str = default_end_date_fnc(),
        frequency: str = None,
        formulas: str = None,
        aggregation: str = None,
        cache: bool = False,
        proxy: str = None,
        proxies: dict = None,
        debug: bool = False,
        api_key: str = None

) -> pd.DataFrame:
    """
    returns all series as pandas DataFrame

    example usages
    template = '''
    TP.ODEMGZS.BDTTOPLAM
    TP.ODEMGZS.ABD
    TP.ODEMGZS.ARJANTIN

    '''

    df = get_series( template )

    df1 = get_series( template , start_date = "01-01-2000" , frequency = "monthly"  )

    df2 = get_series('TP.ODEMGZS.BDTTOPLAM' , start_date = "01-01-2000" , frequency = "monthly"  , cache = True  )

    df3 = get_series( template , start_date = "01-01-2000" , frequency = "monthly" , formulas = "avg"  )

    df3 = get_series( template , start_date = "01-01-2000" , frequency = "monthly" , formulas = ("avg" , "min" , "avg" )  )




    :param index: str or tuple[str]
    :param start_date: str
    :param end_date: str
    :param frequency: str
    :param formulas: str | tuple[str]
    :param aggregation: str| tuple[str]
    :param cache: bool True for using cached data when possible
    :param proxy: str  (default=None)
    :param proxies: dict (default=None)
    :param debug: bool True for debugging
    :return: pd.DataFrame





    """
    if api_key:
        if ApikeyClass().get_valid_api_key(check=False) is False:
            save_apikey(api_key)

    user_req = UserRequest(index,
                           start_date=start_date,
                           end_date=end_date,
                           frequency=frequency,
                           formulas=formulas,
                           aggregation=aggregation,
                           cache=cache,
                           proxy=proxy,
                           proxies=proxies
                           )
    if debug:
        return user_req.dry_request()
    return user_req()


def test_aggr_types(capsys):
    balance_of_pay1 = "TP.ODEMGZS.BDTTOPLAM", "TP.ODEMGZS.ABD"

    balance_of_pay2 = """

    TP.ODEMGZS.BDTTOPLAM #
    TP.ODEMGZS.ABD # 

    """
    cache = True
    with capsys.disabled():
        u1 = UserRequest(balance_of_pay1,
                         frequency="weekly",
                         start_date=default_start_date_fnc(),
                         end_date=default_end_date_fnc(),
                         aggregation=("avg",),
                         # proxy="http://127.0.0.1:8000",
                         # proxies={"http": "http://127.0.0.1:8000"},
                         cache=cache,
                         )

        u2 = UserRequest(balance_of_pay2,
                         frequency="weekly",
                         start_date=default_start_date_fnc(),
                         end_date=default_end_date_fnc(),
                         aggregation=("avg",),
                         # proxy="http://127.0.0.1:8000",
                         # proxies={"http": "http://127.0.0.1:8000"},
                         cache=cache,
                         )
        assert u1 == u2


__all__ = ['get_series']
