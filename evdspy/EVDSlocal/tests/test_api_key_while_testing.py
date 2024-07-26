from evdspy.EVDSlocal.utils.utils_test import get_api_key_while_testing


def test_get_apikey_while_testing():

    a = get_api_key_while_testing()
    assert a
