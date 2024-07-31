import pandas as pd

from evdspy import get_series_exp
from evdspy.EVDSlocal.index_requests.get_series_indexes_exp import Result

index1 = "TP.GSYIH02.GY.CF"
index2 = "TP.GSYIH02.GY.CF"

indexes = """TP_GSYIH01_GY_CF
TP_GSYIH02_GY_CF
TP_GSYIH03_GY_CF
TP_GSYIH04_GY_CF
TP_GSYIH05_GY_CF
TP_GSYIH06_GY_CF
TP_GSYIH07_GY_CF
TP_GSYIH08_GY_CF
TP_GSYIH09_GY_CF
TP_GSYIH10_GY_CF
TP_GSYIH11_GY_CF
TP_GSYIH14_GY_CF
TP_GSYIH15_GY_CF
TP_GSYIH16_GY_CF
"""
index_table = "bie_gsyhgycf"

from typing import Any
import time


def fnc(item: Any) -> Result:
    print(f"  Checking ...  {item}")
    time.sleep(2)
    df = get_series_exp(item, debug=False, cache=True)
    print(df)
    return df


DF = pd.DataFrame


def test_get_series_exp(capsys):
    with capsys.disabled():
        items = [index1, index2, indexes, index_table]

        for item in items:
            result: Result = fnc(item)
            # we will check if this function handles all data types correctly
            # then examine the last one to see what we get as a result from the function
            assert isinstance(result.data, DF)
            assert isinstance(result.metadata, DF)
            assert callable(result.write)
            assert callable(result.to_excel)
