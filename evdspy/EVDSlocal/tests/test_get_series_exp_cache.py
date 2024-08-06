from evdspy import get_series, get_series_exp


def test_get_proxies_env_helper(capsys):
    index = """
    TP.DK.USD.A
    TP.DK.EUR.A
    TP.DK.CHF.A
    TP.DK.GBP.A
    TP.DK.JPY.A


    """

    with capsys.disabled():
        df = get_series(
            index, cache=False, start_date="02-01-2017", end_date="31-12-2017"
        )
        print(df.head())
        res = get_series_exp(
            index, cache=False, start_date="02-01-2017", end_date="31-12-2017"
        )

        # assert df == res.data
        print(res.data)
        assert res.data.shape == df.shape
        # assert res.data.values == df.values 
