
# ------------------------------------------------------------------------------
import requests as requests
from evdspy.EVDSlocal.components.url_class import URLClass
from evdspy.EVDSlocal.utils.utils_general import *
from evdspy.EVDSlocal.requests_.my_cache import MyCache, save_pickle_for_test, lru_cache_patched, load_test_pickle
from evdspy.EVDSlocal.components.options_class import Options
from evdspy.EVDSlocal.config.credentials_file import Credentials
from evdspy.EVDSlocal.initial.start_options import current_mode_is_test
from evdspy.EVDSlocal.initial.start_args import Args
from evdspy.EVDSlocal.messages.error_classes import *
from evdspy.EVDSlocal.config.apikey_class import *
from evdspy.EVDSlocal.config.config import config
from evdspy.EVDSlocal.requests_.my_cache import load_pickle
from evdspy.EVDSlocal.stats.save_stats_of_requests import *
from evdspy.EVDSlocal.requests_.request_error_classes import REQUEST_ERROR_CODES
from evdspy.EVDSlocal.common.url_clean import remove_api_key
from dataclasses import dataclass
from evdspy.EVDSlocal.requests_.mock_req import *
from evdspy.EVDSlocal.requests_.real_requests import *
# ------------------------------------------------------------------------------
m_cache = MyCache()
from evdspy.EVDSlocal.config.config import config
CANCEL_REQUEST_TEMP = config.cancel_request_temp
def do_first_true_order(funcs, preds, url):
    conds = zip(funcs, preds)
    for func, pred in conds:
        if isinstance(pred, bool) and pred:
            v = func(url)
            return v
    return False
def decide_request_for_test_real(url: str, proxies=None):
    """ Finally ready to make request """
    if config.current_mode_is_test and not config.temp_cancel_mock_request:
        """ pytest will get this mock response object"""
        return mock_request(url, proxies)
    # print(f"WARNING : mock results are coming {url}")
    # return mock_request(url, proxies)
    if CANCEL_REQUEST_TEMP:
        print("request was cancelled...")
        return mock_request(url, proxies)
    if proxies is None:
        return requests.get(url)
    return requests.get(url, proxies=proxies)
@dataclass
class EVRequest:
    options_: Options
    session: any = None
    proxy: Optional[str] = False
    args: Args = field(default_factory=Args)  # None  # Args(tuple(sys.argv))
    last_url_checked: str = "NoneURL"
    URL_Instance: field(default_factory=URLClass) = field(default_factory=URLClass)
    force_no_cache = False
    # report : post init
    def __post_init__(self):
        # self.URL_Instance = field(default_factory=URLClass) # None
        self.credentials = Credentials(self.options_)
        """
        we are now reporting how many times
        we requested new items and how many times we avoided making new
        request by using cache results...
        """
        self.report = Report("stats_requests.txt")
    def get_request_with_proxy(self, url: str, proxy: str):
        proxies = {
                'http': proxy,
                'https': proxy,
        }
        return decide_request_for_test_real(url, proxies=proxies)
    def get_proxies(self):
        if self.args.proxy is None:
            return None
        proxy = self.args.proxy
        proxies = {
                'http': proxy,
                'https': proxy,
        }
        return proxies
    def proxy_from_file(self, url: str):
        print("using proxy from file")
        return self.get_request_with_proxy(url, self.args.proxy)
    def proxy_from_cmd_line(self, url: str):
        print("using proxy from commandline")
        return self.get_request_with_proxy(url, self.args.proxy)
    def check_any_apikey(self):
        if not config.current_mode_is_test:
            return True
        if not ApikeyClass().get_valid_api_key():
            raise ApiKeyNotSetError
        return True
    def check_if_request_ok(self, status_code: int):
        corrects = (200,)
        if status_code in corrects:
            self.report.add(f"{status_code} returned. ")
            return True
        self.report.add(f"{status_code} returned. ")
        ExceptionClass = REQUEST_ERROR_CODES.get(status_code, None)
        if ExceptionClass:
            print(ExceptionClass)
            print(f"STATUS CODE : {status_code}\n url : {remove_api_key(self.last_url_checked)}")
            time.sleep(2)
            # raise ExceptionClass(self.__doc__)
        else:
            print(
                    f"Program was checking request status code and noticed "
                    f"{status_code} not included in  `REQUEST_ERROR_CODES`"
            )
        self.report.add(f"{status_code} returned. ")
        return False
    def post_urls(self, url: str) -> tuple:
        # url = url.translate({ord(c): None for c in string.whitespace})
        url = URL_temizle(url)  # whitespace etc.
        no_apikey_url = remove_api_key(url)  # remove key for logs
        self.report.add(f"{no_apikey_url} will be requested. ")
        self.last_url_checked = url
        return (url, no_apikey_url)
    def get_request_alternatives(self, url):
        result = do_first_true_order(
                funcs=[
                        self.proxy_from_cmd_line,
                        self.proxy_from_file,
                        decide_request_for_test_real
                ],
                preds=[
                        self.args.proxy,
                        self.credentials.proxy,
                        True],
                url=url
        )
        return result
    def check_result(self, result):
        if any(
                (
                        not hasattr(result, "status_code"),
                        not isinstance(result.status_code, int),
                        not self.check_if_request_ok(result.status_code)
                )
        ):
            print(f"request returned an error code {result.status_code} , url : {self.no_apikey_url}")
            return False
        return True
    def get_request_before_cache(self, url: str):
        """
        decorated version of this function needs to be
        welcomed by this func to check api key etc.
        TODO
            stats for apikey and results
            warn user if there are many 500 status_code results for the certain api key
        """
        no_apikey_url = remove_api_key(url)
        # print("checking url ... ", no_apikey_url)
        if not self.check_any_apikey():
            return False
        return self.get_request(url)
    def get_request(self, url: str):
        """
        first will check cache if there is cache
        below will not run at all
        """
        # if ApikeyClass().now_testing_is_key_is_valid    :
        #     return self.get_request_by_checking_NO_CACHE(url)
        return self.get_request_by_checking_cache(url)
        # return self.get_request_helper(url )
    @lru_cache_patched
    @m_cache.cache
    def get_request_by_checking_cache(self, url: str):
        """
        """
        return self.get_request_common(url)
    def get_request_by_checking_NO_CACHE(self, url: str):
        """
        """
        return self.get_request_common(url)
    def get_request_w_param(self, url: str, proxies=None):
        return RealRequestWithParam(url, proxies).request()
    def get_request_common(self, url: str):
        """
        first will check cache if there is cache
        below will not run at all
        """
        self.url, self.no_apikey_url = self.post_urls(url)
        if current_mode_is_test and ApikeyClass().key is False:
            print("Current Mode is test not requesting new data see initial.start_options")
            return load_test_pickle()
        """ if it is running we are definitely requesting """
        safe_url = remove_api_key(self.url)
        print("requesting!!", safe_url)
        """ Exception checks will happen in function below"""
        result = self.get_request_w_param(self.url, self.get_proxies())
        # result = self.get_request_alternatives(self.url)
        # result = self.get_request_alternatives(self.no_apikey_url)
        if not self.check_result(result):
            return False
        """ request looks solid we are ready to save """
        if result and self.check_if_request_ok(result.status_code):
            save_pickle_for_test(result)
        return result