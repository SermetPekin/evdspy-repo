import sys

from ..components.evds_files import *
from ..components.evds_seri_files import test_series_
from ..utils.utils_general import *
from ..initial.start_args import Args
from ..components.options_class import Options, load_options
from ..config.apikey_class import *

#from ...main import *

options_ = load_options()
args = Args(sys.argv)
test_evds = EvdsSorgu(
    options_=options_,
    session=None,
    series_=test_series_,
    file_name='pytest_req',
    args=args
)
test_evds_series = EvdsSorguSeries(
    options_,
    session=None,
    series_=test_series_,
    file_name='pytest_req',
    args=args
)




def test_create_class():
    assert test_evds is not None, "test_evds not created"


# def test_evds_save_excel():
#     assert test_evds.kaydet_excel() is True, "test_evds not created"
#
#
# def test_test_evds_series_save_excel():
#     assert test_evds_series.kaydet_excel() is True, "test_evds not created"
#
#
# def test_test_evds_series_save_excel_returns_smt():
#     assert test_evds_series.kaydet_excel() in [True, False], "test_evds not created"
#
folder = get_current_dir()



def test_get_proxy_from_file():
    assert get_proxy_from_file(
        folder / ".." / "tests" / r"test.proxy.txt") == "http://proxy.example.com", "Proxy test failed"


def test_get_api_key():
    assert get_api_key_from_file(folder / ".." / "tests" / r"test.api.txt") == "testApiKey", "Api key test failed"


def test_global_var_api_key():
    assert isinstance(global_var_api_key(), str)
