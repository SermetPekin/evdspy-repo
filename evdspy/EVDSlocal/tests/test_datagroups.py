from evdspy.EVDSlocal.index_requests.datagroups import get_keys


def test_get_keys(capsys):
    with capsys.disabled():
        coming = get_keys()
        print(coming)
