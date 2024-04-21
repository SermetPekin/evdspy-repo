# ....................................................................... DataProcessor
import traceback
from typing import Any

import pandas as pd

from evdspy.EVDSlocal.index_requests.index_util_funcs import make_df_float, json_to_df
from evdspy.EVDSlocal.index_requests.user_requests.User_req_typings import T_maybeDf


class DataProcessor:
    def __init__(self, data: Any):
        self.data = data

    def process_to_dataframe(self) -> T_maybeDf:
        if self.data is False:
            return False
        try:
            df = json_to_df(self.data)
        except Exception as e:
            print(e)
            traceback.print_exc()
            return None
        if isinstance(df, pd.DataFrame):
            df = make_df_float(df)
        return df

    def __call__(self, *args, **kwargs) -> T_maybeDf:
        return self.process_to_dataframe()


def test_DataProcessor(capsys):
    with capsys.disabled():
        d = DataProcessor(False)
        print(d)
