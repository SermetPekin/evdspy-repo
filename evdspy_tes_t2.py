
from evdspy import *
import pandas as pd  
def get_api_key():
    import os
    return os.getenv("EVDS_API_KEY")
assert isinstance(get_api_key(), str) and len(get_api_key()) == 10
def t1():
    setup()
    save(get_api_key())
def t2():
    from evdspy.main import get_df_datagroup
    df = get_df_datagroup(
        datagroup="bie_gsyhgycf",
        start_date="01-01-1998",
        end_date="01-01-2030",
    )
    print(df)
    assert isinstance(df, pd.DataFrame)
if __name__ == "__main__":
    t1()
    t2()