
def test1_real_reqs():
    from evdspy.EVDSlocal.index_requests.get_series_indexes import UserRequest, default_start_date_fnc, \
        default_end_date_fnc
    """
    TP.BFTUKKRE.L001	TP.BFTUKKRE.L010	TP.BFTUKKRE.L011	TP.BFTUKKRE.L012
    """
    credits_template = ("TP.BFTUKKRE.L001", "TP.BFTUKKRE.L010", "TP.BFTUKKRE.L011", "TP.BFTUKKRE.L012",)
    ur = UserRequest("TP.ODEMGZS.BDTTOPLAM")
    print(ur.url)
    assert ur.url == "https://evds2.tcmb.gov.tr/service/evds/series=TP.ODEMGZS.BDTTOPLAM&startDate=01-01-2000&endDate=01-01-2100&type=json"
    print(ur)
    balance_of_pay = "TP.ODEMGZS.BDTTOPLAM", "TP.ODEMGZS.ABD"
    cache = False
    ur = UserRequest(balance_of_pay,
                     frequency="weekly",
                     start_date=default_start_date_fnc(),
                     end_date=default_end_date_fnc(),
                     aggregation=("avg",),
                     proxy="http://127.0.0.1:8000",
                     proxies={"http": "http://127.0.0.1:8000"},
                     cache=cache)
    ur.dry_request()
    d1 = ur()
    print(d1)
    ur = UserRequest(credits_template,
                     frequency="weekly",
                     start_date=default_start_date_fnc(),
                     end_date=default_end_date_fnc(),
                     aggregation=("avg",),
                     proxy="http://127.0.0.1:8000",
                     proxies={"http": "http://127.0.0.1:8000"},
                     cache=cache)
    print(ur.url)
    # result = ur.request()
    ur.dry_request()
    d2 = ur()
    print(d2)
    return d1, d2