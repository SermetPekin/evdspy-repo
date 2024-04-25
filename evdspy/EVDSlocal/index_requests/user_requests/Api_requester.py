# ...........................................................................................
import traceback
import requests
# ...........................................................................................
from evdspy.EVDSlocal.index_requests.user_requests.Url_builder import UrlBuilder 
from evdspy.EVDSlocal.index_requests.user_requests.Proxy_manager import ProxyManager 
from evdspy.EVDSlocal.index_requests.user_requests.Request_config import RequestConfig
from evdspy.EVDSlocal.index_requests.user_requests.User_request_utils import cache_or_raw_fnc
from evdspy.EVDSlocal.utils.utils_test import ApiClassWhileTesting
from evdspy.EVDSlocal.requests_.real_requests import *
from evdspy.EVDSlocal.utils.github_actions import PytestTesting, GithubActions

# ...........................................................................................


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
