from evdspy.EVDSlocal.requests_.ev_request import *

from ..tests.core_options_test import *


def test_mock_request2(capsys):
    response = mock_request("test_url")


    with capsys.disabled():
        if verbose:
            #print(response , type(response))
            print(type(response ))
    assert isinstance(response, requests.models.Response)

def test_report2():
    report_test()


