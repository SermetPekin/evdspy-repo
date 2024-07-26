
# ------------------------------------------------------------------------------
import requests as requests
from evdspy.EVDSlocal.utils.utils_general import *
from evdspy.EVDSlocal.requests_.my_cache import MyCache
from evdspy.EVDSlocal.messages.error_classes import *
from evdspy.EVDSlocal.config.apikey_class import *
from evdspy.EVDSlocal.config.config import config
from evdspy.EVDSlocal.requests_.my_cache import load_pickle
from evdspy.EVDSlocal.stats.save_stats_of_requests import *
# ------------------------------------------------------------------------------
m_cache = MyCache()
CANCEL_REQUEST_TEMP = config.cancel_request_temp
def mock_request(url, proxies=None) -> requests.models.Response:
    """ pytest will get this mock response object"""
    assert isinstance(url, str)
    file_name = str(Path(__file__).parent / "test_reg_result")
    assert Path(file_name + ".pickle").is_file(), f"file does not exist {file_name}"
    return load_pickle(file_name)