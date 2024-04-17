from evdspy import *

from evdspy import get_series, default_start_date_fnc, default_end_date_fnc


def get_api_key():
    import os
    return os.getenv("EVDS_API_KEY")


if not get_api_key():
    raise Exception("No API key provided from environment variables")


def test1():
    setup()
    save(get_api_key())


def test2():
    df = get_series("TP.ODEMGZS.BDTTOPLAM",
                    frequency="monthly",
                    start_date=default_start_date_fnc(),
                    end_date=default_end_date_fnc(),
                    aggregation=("avg",),
                    cache=False,
                    debug=False,
                    api_key=get_api_key())
    print(df)
    assert isinstance(df, pd.DataFrame)


if __name__ == "__main__":
    if not get_api_key():
        raise Exception("No API key provided from environment variables")
    test1()
    test2()
