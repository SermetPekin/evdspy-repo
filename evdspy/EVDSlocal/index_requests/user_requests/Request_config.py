# ................................................................... RequestConfig
from dataclasses import dataclass
from typing import Union, Optional

# from evdspy import default_start_date_fnc, default_end_date_fnc
from evdspy.EVDSlocal.components.excel_class import replace_all
from evdspy.EVDSlocal.index_requests.get_series_indexes_utils import freq_enum, correct_types, AggregationType, \
    Formulas, default_start_date_fnc, default_end_date_fnc
from evdspy.EVDSlocal.index_requests.user_requests.Serialize import Serialize
from evdspy.EVDSlocal.index_requests.user_requests.User_req_typings import T_tuple_str_int_None, T_str_tuple_None, \
    T_str_int_None
from evdspy.EVDSlocal.index_requests.user_requests.User_request_utils import UserRequestUtils


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
