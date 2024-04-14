import evdspy
from evdspy.EVDSlocal.main_ import *

def test_load_general():
    assert callable(setup_series), "setup_series is not callable"
    assert callable(help_), "help_ is not callable"


def test_setup_now():
    # evdspy.setup_now()
    # evdspy.help_()
    # evdspy.check()
    easy_setup()
    get()


from evdspy.EVDSlocal.config.apikey_class import ApikeyClass


def test_set_apikey():
    assert ApikeyClass().set_api_key_filetype(value="test") == "test", "set api key did not work"
    assert ApikeyClass().set_api_key_runtime(value="testruntime") == "testruntime", "set api key did not work"


def test_get_apikey():
    assert ApikeyClass().set_api_key_filetype(value="test") == "test", "get api key did not work"
    assert ApikeyClass().get_api_key_fromfile() == "test", "get api key did not work"
    assert ApikeyClass().set_api_key_filetype("test3") == "test3", "set api key did not work"
    assert ApikeyClass().get_api_key_fromfile() == "test3", "get api3 key did not work"
    assert ApikeyClass().get_api_key_runtime() == "testruntime", "get testruntime  key did not work"

def test_valid_key():
    assert ApikeyClass().set_api_key_filetype(value="thatisfromFile") == "thatisfromFile", "get api key did not work"
    ApikeyClass().now_testing_is_key_is_valid = "thisisValid"
    # assert ApikeyClass().get_valid_api_key() == "thisisValid", "get thisisValid  key did not work"
