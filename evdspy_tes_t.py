from evdspy import *

from evdspy import get_series, default_start_date_fnc, default_end_date_fnc


def get_api_key():
    import os
    return os.getenv("EVDS_API_KEY")


assert isinstance(get_api_key(), str) and len(get_api_key()) == 10


def t1():
    setup()
    save(get_api_key())


def t2():
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
    t1()
    t2()
