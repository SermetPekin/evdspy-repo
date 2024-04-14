from evdspy.EVDSlocal.requests_.lower_energy import apikey_works


def test_apikey_worksM():
    assert apikey_works("s1") is True, "s1 is not True"
    assert apikey_works("f1") is False, "s1 is not True"
