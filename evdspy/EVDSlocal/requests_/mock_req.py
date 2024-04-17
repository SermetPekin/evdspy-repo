
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
# ------------------------------------------------------------------------------
m_cache = MyCache()
from evdspy.EVDSlocal.config.config import config
CANCEL_REQUEST_TEMP = config.cancel_request_temp
def mock_request(url, proxies=None) -> requests.models.Response:
    """ pytest will get this mock response object"""
    assert isinstance(url, str)
    file_name = str(Path(__file__).parent / "test_reg_result")
    assert Path(file_name + ".pickle").is_file(), f"file does not exist {file_name}"
    return load_pickle(file_name)