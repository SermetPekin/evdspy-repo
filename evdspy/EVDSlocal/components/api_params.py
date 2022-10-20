from typing import Callable, List, Union, Tuple
from dataclasses import dataclass, field
from abc import ABC, abstractmethod
from enum import Enum
from typing import Callable, Protocol, List, Tuple, Union
from datetime import datetime

default_api_domain = "https://evds2.tcmb.gov.tr/service/evds/"


@dataclass
class ApiDomain(ABC):
    domain: str


@dataclass
class EVDSApiDomain(ApiDomain):
    domain: str = default_api_domain

    def __repr__(self):
        return self.domain


# --------------------------------Frequency---------------------
class FrequencyEnum(Enum):
    daily = 1
    business_day = 2
    weekly = 3
    semimonthly = 4
    monthly = 5
    quarterly = 6
    semi_annual = 7
    annual = 8
    default = 5


class AggregationEnum(Enum):
    average = "avg"
    min = "min"
    max = "max"
    first = "first"
    last = "last"
    cumulative = "sum"
    default = "avg"


class FormulasEnum(Enum):
    level = 0
    percentage_change = 1
    difference = 2
    yoy_percentage_change = 3
    yoy_difference = 4
    per_cha_com_end_of_pre_yea = 5
    dif_com_end_of_pre_yea = 6
    moving_average = 7
    moving_sum = 8
    default = 0


from typing import Callable


def get_enum_with_value(key: Union[str, int], enum_: Union[str, int, Callable], default_value=None) -> Union[str, int]:
    """ typical usages
        get_enum_with_value( 5 , Frequency , Frequency.Monthly )

    """
    if isinstance(key, int):
        key = str(key)

    if hasattr(default_value, "value"):
        """otherwise probably None """
        default_value = getattr(default_value, "value", None)

    dd = {str(x.value): x for x in enum_}
    enum_value: Enum = dd.get(key, None)

    if hasattr(enum_value, "value"):
        v = getattr(enum_value, "value")
        return v
    if not default_value:
        return getattr(default_value, "default")
    return default_value


@dataclass
class UrlParam(ABC):
    """UrlParam class """
    value: Union[str, datetime, int, Tuple[str], Callable, Enum, List[str]]
    initial: str = "anything"
    number_of_repeat: int = 1
    disp_value: str = ""
    required: bool = True
    obscured: bool = False

    def __str__(self) -> str:
        return f"{self.disp_value}"

    def __repr__(self) -> str:
        return f"{self.disp_value}"

    def __post_init__(self):
        self.create_disp_value()

    def create_disp_value(self):
        if not self.value:
            self.disp_value = f"{self.initial}=Noneapi.params.103"
            return

        # if isinstance(self.value, Enum) :
        if hasattr(self.value, "value"):
            self.disp_value = f"{self.initial}={self.value.value}"
        if isinstance(self.value, (tuple, list,)):
            value: str = "-".join(self.value)
            self.disp_value = f"{self.initial}={value}"
            return
        if isinstance(self.value, (str, int,)):
            self.disp_value = f"{self.initial}={self.value}"
            return
        if self.value is None:
            if self.required:
                raise f"{self.__class__.__name__} parameter is required"
            return
        self.disp_value = f"{self.initial}={self.value}"

    def reportable_value(self):
        if self.obscured:
            return f"{self.initial}=obscured_for_report"
        return self.disp_value

    def explanation(self):
        if self.obscured:
            return f"{self.initial}: obscured_for_report"
        if callable(self.value):
            disp_value = f"{self.initial}: {self.value.__name__}"
            return disp_value
        if isinstance(self.value, (list, str,)):
            disp_value = f"{self.initial}: {', '.join(self.value)}"
            return disp_value
        return f"{self.initial}: {self.value}"


@dataclass
class Apikey(UrlParam):
    initial: str = "key"
    obscured: bool = True


@dataclass
class Series(UrlParam):
    """ Frequency """
    initial: str = "series"
    value: Union[List[str], Tuple[str]] = ()


@dataclass
class Frequency(UrlParam):
    """ Frequency """
    # value: Union[str, datetime, int, Tuple, Callable, Enum]
    initial: str = "frequency"
    required: bool = False


@dataclass
class Formulas(UrlParam):
    """ Formulas """
    initial: str = "formulas"
    required: bool = False

    def create_disp_value(self):
        repeat = "-".join([str(self.value) for x in range(self.number_of_repeat)])
        self.disp_value = f"{self.initial}={repeat}"


@dataclass
class Aggregations(UrlParam):
    """ Aggregations """
    initial: str = "aggregationTypes"
    required: bool = False

    def create_disp_value(self):
        repeat = "-".join([str(self.value) for x in range(self.number_of_repeat)])
        self.disp_value = f"{self.initial}={repeat}"


@dataclass
class DateStart(UrlParam):
    """ DateStart """
    initial: str = "startDate"


@dataclass
class DateEnd(UrlParam):
    """ DateEnd """
    value: str = ""
    initial: str = "endDate"


def convert_list_params_to_str(alist: Union[List[UrlParam], Tuple[UrlParam]], fnc: Union[Callable, str] = str):
    separator_char = "&"
    if fnc == str:
        alist = [str(x) for x in alist if x is not None]
        alist_str: str = separator_char.join(alist)
    else:
        indent = " " * 10
        block = "-" * 25
        separator_char = "\n" + indent
        if fnc == "report":
            alist = [x.reportable_value() for x in alist if x.reportable_value() is not None]
        if fnc == "explanation":
            alist = [x.explanation() for x in alist if x.explanation() is not None]
        alist_str: str = block + f"{fnc}" + block + "\n" + indent + separator_char.join(alist)
    return alist_str
