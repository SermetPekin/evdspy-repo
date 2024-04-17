
from ..components.url_class import *
from ..components.api_params import *
from ..components.api_params import EVDSApiDomainCategories, ModeParamDataGroups, CodeParamDataGroups
from ..config.apikey_class import ApikeyClass
from dataclasses import dataclass
from ..requests_.ev_request import EVRequest
from ..messages.error_classes import ApiKeyNotSetError
from ..components.options_class import SingletonOptions
import typing as t
@dataclass
class GeneralIndexesBase(ABC):
    """GeneralIndexesBase"""
    domain: t.Union[str, EVDSApiDomain]
    EVRequest_: EVRequest = None
    type_param: dataTypeEnum = dataTypeEnum.csv  # csv or json
    mode: ModeEnumDatagroup = ModeEnumDatagroup.all_groups
    code: int = 1
    # EVRequest_: EVRequest = EVRequest()
    def __repr__(self):
        res = f"""
class : [{self.__class__.__name__} ]
mode :  [{self.mode}]
code : [{self.code}]
url : [{self.EVRequest_.URL_Instance.url}]
"""
        return res
    def __str__(self):
        res = f"""
class : [{self.__class__.__name__} ]
mode :  [{self.mode}]
code : [{self.code}]
url : [{self.EVRequest_.URL_Instance.url}]
"""
        return res
    def create_url_first_part(self):
        self.api_key = ApikeyClass().get_valid_api_key()
        full_list = []
        self.complete_url_instance = URLClass(full_list, domain=str(self.domain))
        self.complete_url_instance.add_apikey(self.api_key)
        # self.complete_url_instance.add_item(dataTypeParam(self.type_param))
    def create_url(self):
        self.create_url_first_part()
        self.add_extra_params()
        self.complete_url_instance.refresh_url()
        self.complete_url_instance.create_report()
        self.EVRequest_.URL_Instance = self.complete_url_instance
        if not self.api_key:
            raise ApiKeyNotSetError
        return self.complete_url_instance.url
    def add_extra_params(self, mode: int = 1, code: t.Union[int, str] = None):
        ...
    def get_csv(self, url: str = None):
        self.create_url()
        if url is None:
            url = self.EVRequest_.URL_Instance.url
        self.EVRequest_.URL_Instance = self.complete_url_instance
        result = self.EVRequest_.get_request_before_cache(f"{url}&type=csv")
        if hasattr(result, "text"):
            self.csv = result.text
            return result.text
        return False
    def get_json(self, url: str = None):
        # raise NotImplementedError
        self.create_url()
        if url is None:
            url = self.EVRequest_.URL_Instance.url
        self.EVRequest_.URL_Instance = self.complete_url_instance
        result = self.EVRequest_.get_request_before_cache(f"{url}&type=json")
        if hasattr(result, "json"):
            self.csv = result.json()
            return result.json()
        return False
class dataGroupsNeedsCode(BaseException):
    """dataGroupsNeedsCode"""
@dataclass
class GeneralIndexesCategories(GeneralIndexesBase):
    """GeneralIndexesCategories"""
    domain: t.Union[str, EVDSApiDomain] = field(default_factory=EVDSApiDomainCategories)
@dataclass
class GeneralIndexesDatagroups(GeneralIndexesBase):
    """GeneralIndexesDatagroups"""
    domain: t.Union[str, EVDSApiDomain] = field(default_factory=EVDSApiDomainDatagroups)
    def add_extra_params(self, mode: int = 2, code: int = None):
        self.complete_url_instance.add_mode(mode)
        if code is None:
            code = self.code
        self.complete_url_instance.add_code(code)
@dataclass
class GeneralIndexesDatagroupIndividual(GeneralIndexesBase):
    """GeneralIndexesDatagroups"""
    domain: t.Union[str, EVDSApiDomain] = field(default_factory=EVDSApiDomainDatagroupIndividual)
    def add_extra_params(self, mode: int = 2, code: str = None):
        ...
        self.complete_url_instance.add_frame(code)
        # self.complete_url_instance.add_mode(mode)
        # if code is None:
        #     code = self.code
        # self.complete_url_instance.add_code(code)
    def get_json(self, url: str = None):
        if url is None:
            url = self.complete_url_instance.url
        result = self.EVRequest_.get_request_before_cache(f"{url}&type=json")
        if hasattr(result, "json"):
            self.csv = result.json()
            return result.json()
        return False
@dataclass
class GeneralIndexesDatagroupSeriesList(GeneralIndexesDatagroupIndividual):
    """GeneralIndexesDatagroups"""
    domain: t.Union[str, EVDSApiDomain] = field(default_factory=EVDSApiDominDatagroupSeriesList)
    def add_extra_params(self, mode: int = 2, code: str = None):
        self.complete_url_instance.add_code(code)
    def get_json(self, url: str = None):
        if url is None:
            url = self.complete_url_instance.url
        result = self.EVRequest_.get_request_before_cache(f"{url}&type=json")
        if hasattr(result, "json"):
            self.csv = result.json()
            return result.json()
        return False