
from evdspy.EVDSlocal.manual_requests.prepare import PrepareUrl
def test_prep(capsys):
    p = PrepareUrl(series=('TP_ODEMGZS_NORVEC-8',), api_key='api_key')
    # with capsys.disabled():
    #     p = PrepareUrl(series=('TP_ODEMGZS_NORVEC-8',), api_key='api_key')
    #     #print(p.get_data())