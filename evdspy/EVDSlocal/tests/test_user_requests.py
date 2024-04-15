from evdspy.EVDSlocal.index_requests.get_series_indexes import UserRequest, default_start_date_fnc, \
    default_end_date_fnc, get_series, Frequency, freq_enum
from evdspy.EVDSlocal.utils.utils_test import get_api_key_while_testing


def test_template_series(capsys):
    with capsys.disabled():
        balance_of_pay1 = "TP.ODEMGZS.BDTTOPLAM", "TP.ODEMGZS.ABD"

        balance_of_pay2 = """

        TP.ODEMGZS.BDTTOPLAM #
        TP.ODEMGZS.ABD # 

        """
        a1 = get_series(balance_of_pay1, debug=True)
        a2 = get_series(balance_of_pay2, debug=True)
        print(a1.hash, a2.hash)

        assert a1 == a2


def test_template_series2(capsys):
    with capsys.disabled():
        balance_of_pay1 = "TP.ODEMGZS.BDTTOPLAM", "TP.ODEMGZS.ABD"

        balance_of_pay2 = """

        TP.ODEMGZS.BDTTOPLAM #
        TP.ODEMGZS.ABD # 

        """
        a1 = get_series(balance_of_pay1, aggregation="avg", debug=True)
        a2 = get_series(balance_of_pay2, aggregation=("avg", "avg"), debug=True)
        print(a1.hash, a2.hash)

        assert a1 == a2


def test_template_series3(capsys):
    with capsys.disabled():
        balance_of_pay1 = "TP.ODEMGZS.BDTTOPLAM", "TP.ODEMGZS.ABD"

        balance_of_pay2 = """

        TP.ODEMGZS.BDTTOPLAM #
        TP.ODEMGZS.ABD # 

        """
        a1 = get_series(balance_of_pay1, formulas="level", debug=True)
        a2 = get_series(balance_of_pay2, formulas=(0, 0), debug=True)
        print(a1.hash, a2.hash)

        assert a1 == a2


def test_freq(capsys):
    f = Frequency.annually

    with capsys.disabled():
        assert f() == "&frequency=8"
        print("\n")
        print(f())
        g = freq_enum("daily")
        assert g == "&frequency=1"
        assert freq_enum("daily") == "&frequency=1"
        assert freq_enum("monthly") == "&frequency=5"
        assert freq_enum("annual") == "&frequency=8"
        assert freq_enum(3) == "&frequency=3"
        assert freq_enum(1) == "&frequency=1"


def test_pickles():
    import os
    os.makedirs("pickles", exist_ok=True)


def test_get_api_key_while_testing(capsys):
    with capsys.disabled():
        a = get_api_key_while_testing()
        assert len(a) > 5 and 'lg' in a


def test_get_series(capsys):
    with capsys.disabled():
        index = 'TP.YSSK.A1'
        start_date = "01-01-2000"
        end_date = "01-01-2100"
        cache = True
        # user_req = UserRequest(index, start_date, end_date)
        df = get_series(index, start_date, end_date, cache)
        print(df)


def test_UserRequest(capsys):
    with capsys.disabled():
        print("\n")
        ur = UserRequest("TP.ODEMGZS.BDTTOPLAM")
        assert ur.url == "https://evds2.tcmb.gov.tr/service/evds/series=TP.ODEMGZS.BDTTOPLAM&startDate=01-01-2000&endDate=01-01-2100&type=json"
        ur = UserRequest(("Aaa", "Bbb",),
                         start_date=default_start_date_fnc(),
                         end_date=default_end_date_fnc(),
                         aggregation=("avg",))
        assert ur.url == "https://evds2.tcmb.gov.tr/service/evds/series=Aaa-Bbb&aggregationTypes=avg-avg&startDate=01-01-2000&endDate=01-01-2100&type=json"

        ur = UserRequest(("Aaa", "Bbb",),
                         start_date=default_start_date_fnc(),
                         end_date=default_end_date_fnc(),
                         aggregation=("avg",),
                         formulas="level")
        assert ur.url == "https://evds2.tcmb.gov.tr/service/evds/series=Aaa-Bbb&formulas=level-level&aggregationTypes=avg-avg&startDate=01-01-2000&endDate=01-01-2100&type=json"

        ur = UserRequest(("Aaa", "Bbb",),
                         frequency=3,
                         start_date=default_start_date_fnc(),
                         end_date=default_end_date_fnc(),
                         aggregation=("avg",),
                         formulas="level")
        print(ur.url)
        assert ur.url == "https://evds2.tcmb.gov.tr/service/evds/series=Aaa-Bbb&frequency=3&formulas=level-level&aggregationTypes=avg-avg&startDate=01-01-2000&endDate=01-01-2100&type=json"
