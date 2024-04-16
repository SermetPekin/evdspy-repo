
from dataclasses import dataclass, field
from typing import List, Tuple, Union
from evdspy.EVDSlocal.components.api_params import UrlParam, convert_list_params_to_str, EVDSApiDomain, Apikey, \
    Frequency, \
    get_enum_with_value, FrequencyEnum, FormulasEnum, Formulas, AggregationEnum, Aggregations
from evdspy.EVDSlocal.components.api_params import *
import typing as t
from enum import Enum
from .api_params_enums import get_enum_with_value
from ..config.apikey_class import ApikeyClass
class ApiParamsNotExpectedFormat(BaseException):
    """ApiParamsNotExpectedFormat"""
@dataclass
class URLClass:
    url_items: Union[List[UrlParam], Tuple[UrlParam]] = field(default_factory=list)
    url: str = None
    url_only_required = None
    url_items_required = None
    url_report: str = ""
    url_explanation: str = ""
    domain: str = str(EVDSApiDomain())
    def __post_init__(self):
        self.url_items_required = tuple(x for x in self.url_items if x.required)
        self.refresh_url()
    def safe_to_report_url(self, url_parts=None):
        if url_parts is None:
            url_parts = self.url_items
        url_parts = [x for x in url_parts if not x.hidden]
        url: str = str(self.domain) + convert_list_params_to_str(url_parts, str)
        return url
    def create_report(self, url_parts=None):
        if url_parts is None:
            url_parts = self.url_items
        self.url_report = convert_list_params_to_str(url_parts, "report")
        self.url_explanation = convert_list_params_to_str(url_parts, "explanation")
        return [self.url_report, self.url_explanation]
    def create_url(self, url_parts: Union[List, Tuple] = None):
        """both for required and complete """
        if url_parts is None:
            url_parts = self.url_items
        url: str = str(self.domain) + convert_list_params_to_str(url_parts, str)
        return url
    def refresh_required(self):
        self.url_items_required = tuple(x for x in self.url_items if x.required)
    def refresh_url(self):
        self.create_url_complete()
        self.create_url_required()
        # self.create_report()
    def create_url_complete(self):
        self.url: str = self.create_url(self.url_items)
    def create_url_required(self):
        self.url_only_required: str = self.create_url(self.url_items_required)
    def add_item(self, item: UrlParam) -> None:
        self.url_items = list(self.url_items) + [item]
        self.refresh_required()
        self.refresh_url()
    def add_frame(self, code_str: str):
        self.add_item(DataGroup(code_str))
        self.refresh_url()
    def add_apikey(self, api_key=None):
        """ Not needed because apikey was moved to header """
        return
        # if api_key is None:
        #     api_key = ApikeyClass().get_valid_api_key()
        # self.add_item(Apikey(api_key))
        # self.refresh_url()
    def add_mode(self, mode_enum: t.Union[Enum, str, int] = 1):
        mode_enum = get_enum_with_value(mode_enum, ModeEnumDatagroup, ModeEnumDatagroup.all_groups)
        self.add_item(ModeParamDataGroups(mode_enum))
        self.refresh_url()
    def add_code(self, code: t.Union[int, str]):
        self.add_item(CodeParamDataGroups(code))
        self.refresh_url()
    def add_frequency(self, frequency: Union[int, str]):
        if isinstance(frequency, str):
            frequency = int(frequency)
        self.add_item(Frequency(get_enum_with_value(frequency, FrequencyEnum)))
        self.refresh_url()
    def add_formulas(self, formulas: Union[int, str], number_of_series: int):
        if isinstance(formulas, str):
            formulas = int(formulas)
        self.add_item(Formulas(get_enum_with_value(formulas, FormulasEnum), number_of_repeat=number_of_series))
        self.refresh_url()
    def add_aggtype(self, aggtype: str, number_of_series: int):
        self.add_item(Aggregations(get_enum_with_value(aggtype, AggregationEnum), number_of_repeat=number_of_series))
        self.refresh_url()