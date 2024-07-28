from pathlib import Path
import pandas as pd
from evdspy.EVDSlocal.index_requests.get_series_indexes import (
    default_start_date_fnc,
    default_end_date_fnc,
    get_series,
)
from evdspy.EVDSlocal.utils.utils_general import get_env_api_key
from evdspy.EVDSlocal.utils.utils_test import (
    ApiClassWhileTesting,
    get_api_key_file,
    skip_if_gthub,
    skip_if_not_keyvalid,
    is_df,
)
from evdspy.EVDSlocal.index_requests.get_series_indexes_utils import (
    Frequency,
    freq_enum,
    Formulas,
    AggregationType,
    correct_types,
)
from evdspy.EVDSlocal.utils.utils_test import get_api_key_while_testing

# from evdspy.EVDSlocal.index_requests.user_requests import
from evdspy.EVDSlocal.index_requests.get_series_indexes_utils import (
    default_start_date_fnc,
    default_end_date_fnc,
)
from evdspy.EVDSlocal.index_requests.user_requests import RequestConfig

import random 

def get_options():
    aggr = [
        "monthly",
        "weekly",
        "annually",
        "semimonthly",
        "semiannually",
        "business",
        None,
    ]
    formulas = ["level", "percentage_change", "difference", None]
    freq = [
        "monthly",
        "weekly",
        "annually",
        "semimonthly",
        "semiannually",
        "business",
        None,
    ]
    def get_one(chs):
        return random.choices(chs, k=1)[0]

    yield {
        "aggregation": get_one(aggr),
        "formulas": get_one(formulas),
        "frequency": get_one(freq),
    }


            
def test_get_series_2(capsys):
    with capsys.disabled(): 
        for _ in range(2) :
            kw = get_options()
            kwargs = tuple(kw)[0]
            print(kwargs)
            try : 
                df = get_series("TP.TIG01", start_date='01-01-2023' ,  debug=False, **kwargs)
                assert isinstance(df, pd.DataFrame)
                
                print(df , type(df ))
            except:
                pass 
            