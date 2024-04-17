
from dataclasses import dataclass, field
from abc import ABC, abstractmethod
from enum import Enum
from typing import Callable, List, Tuple, Union
from datetime import datetime
from evdspy.EVDSlocal.components.api_params_enums import *
default_api_domain = "https://evds2.tcmb.gov.tr/service/evds/"
@dataclass
class ApiDomain(ABC):
    domain: str
@dataclass
class EVDSApiDomain(ApiDomain):
    domain: str = default_api_domain
    def __repr__(self):
        return self.domain
@dataclass
class EVDSApiDomainCategories(ApiDomain):
    domain: str = f"{default_api_domain}categories/"
    def __repr__(self):
        return self.domain
@dataclass
class EVDSApiDomainDatagroups(ApiDomain):
    domain: str = f"{default_api_domain}datagroups/"
    def __repr__(self):
        return self.domain
@dataclass
class EVDSApiDomainDatagroupIndividual(ApiDomain):
    domain: str = f"{default_api_domain}"  # datagroup=bie_yssk
    def __repr__(self):
        return self.domain
# GeneralIndexesDatagroupSeriesList
@dataclass
class EVDSApiDominDatagroupSeriesList(ApiDomain):
    domain: str = f"{default_api_domain}serieList/"  # serieList/key=xxx&type=json&code=bieyssk
    def __repr__(self):
        return self.domain
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
        if not self.value and str(self.value) != "0":
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
        if not self.value:
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
from typing import Callable
@dataclass
class Apikey(UrlParam):
    initial: str = "key"
    obscured: bool = True
class DecimalSeparator(UrlParam):
    value: Separator = Separator.period
    initial: str = "DecimalSeparator"
@dataclass
class Series(UrlParam):
    """ Frequency """
    value: Union[List[str], Tuple[str]] = ()
    initial: str = "series"
@dataclass
class DataGroup(UrlParam):
    """ Frequency """
    value: str = ''
    initial: str = "datagroup"
    required: bool = True
    def create_disp_value(self):
        self.disp_value = f"{self.initial}={self.value}"
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
    value: str = ""
    initial: str = "startDate"
@dataclass
class DateEnd(UrlParam):
    """ DateEnd """
    value: str = ""
    initial: str = "endDate"
@dataclass
class dataTypeParam(UrlParam):
    value: dataTypeEnum = dataTypeEnum.csv
    required = True
    initial: str = "type"
    def create_disp_value(self):
        self.disp_value = f"{self.initial}={self.value.value}"
@dataclass
class ModeParamDataGroups(UrlParam):
    initial: str = "mode"
    required = True
    # def create_disp_value(self):
    #     self.disp_value = f"{self.initial}={self.value.value}"
@dataclass
class CodeParamDataGroups(UrlParam):
    value = 0
    initial: str = "code"
    required = True
    def create_disp_value(self):
        if hasattr(self.value, "value"):
            value = self.value.value
        else:
            value = self.value
        self.disp_value = f"{self.initial}={value}"
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