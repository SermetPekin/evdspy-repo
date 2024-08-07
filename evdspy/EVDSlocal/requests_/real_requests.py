
# ------------------------------------------------------------------------------
import requests as requests
from evdspy.EVDSlocal.utils.utils_general import *
from evdspy.EVDSlocal.requests_.my_cache import MyCache
from evdspy.EVDSlocal.messages.error_classes import *
from evdspy.EVDSlocal.config.apikey_class import *
from evdspy.EVDSlocal.config.config import config
from evdspy.EVDSlocal.stats.save_stats_of_requests import *
# ------------------------------------------------------------------------------
m_cache = MyCache()
CANCEL_REQUEST_TEMP = config.cancel_request_temp
from evdspy.EVDSlocal.requests_.mock_req import *
class RealRequest(object):
    """ pytest will get this mock response object"""
    def __init__(self, url: str, proxies=None, api_key=False):
        self.url = url
        self.proxies = proxies
        if not api_key:
            self.api_key = ApikeyClass().key
        else:
            self.api_key = api_key
    def request_no_proxy(self) -> requests.Response:
        return requests.get(self.url)
    def request_proxy(self) -> requests.Response:
        return requests.get(self.url, proxies=self.proxies)
    def request(self) -> requests.Response:
        if config.current_mode_is_test and not config.temp_cancel_mock_request:
            """ pytest will get this mock response object"""
            return mock_request(self.url, self.proxies)
        if self.proxies is None:
            return self.request_no_proxy()
        return self.request_proxy()
class RealRequestWithParam(RealRequest):
    def get_header(self) -> dict:
        # api_key = ApikeyClass().key
        headers = {
            "key": self.api_key
        }
        return headers
    def request_no_proxy(self) -> requests.Response:
        headers = self.get_header()
        # print(headers)
        # print(self.url)
        response = requests.get(self.url, headers=headers)
        return response
    def request_proxy(self) -> requests.Response:
        headers = self.get_header()
        return requests.get(self.url, headers=headers, proxies=self.proxies)
    def request(self) -> requests.Response:
        if config.current_mode_is_test and not config.temp_cancel_mock_request:
            """ pytest will get this mock response object"""
            return mock_request(self.url, self.proxies)
        if self.proxies is None:
            return self.request_no_proxy()
        return self.request_proxy()