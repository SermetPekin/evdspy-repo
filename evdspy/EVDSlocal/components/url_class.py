from dataclasses import dataclass, field
from typing import List, Tuple, Union
from evdspy.EVDSlocal.components.api_params import UrlParam, convert_list_params_to_str, EVDSApiDomain, Apikey, \
    Frequency, \
    get_enum_with_value, FrequencyEnum, FormulasEnum, Formulas, AggregationEnum, Aggregations
@dataclass
class URLClass:
    url_items: Union[List[UrlParam], Tuple[UrlParam]] = field(default_factory=List[UrlParam])
    url: str = None
    url_only_required = None
    url_items_required = None
    url_report: str = ""
    url_explanation: str = ""
    def __post_init__(self):
        self.url_items_required = tuple(x for x in self.url_items if x.required)
        self.refresh_url()
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
        url: str = str(EVDSApiDomain()) + convert_list_params_to_str(url_parts, str)
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
    def add_item(self, item):
        self.url_items = list(self.url_items) + [item]
        self.refresh_required()
        self.refresh_url()
    def add_apikey(self, api_key):
        self.add_item(Apikey(api_key))
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
