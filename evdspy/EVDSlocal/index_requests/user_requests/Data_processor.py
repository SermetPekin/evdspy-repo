# ....................................................................... DataProcessor
import traceback
from typing import TYPE_CHECKING, Any

import pandas as pd

from evdspy.EVDSlocal.index_requests.index_util_funcs import make_df_float, json_to_df
from evdspy.EVDSlocal.index_requests.user_requests.User_req_typings import T_maybeDf
from evdspy.EVDSlocal.index_requests.index_util_funcs import try_date

if TYPE_CHECKING:

    from evdspy.EVDSlocal.index_requests.user_requests import RequestConfig


class DataProcessor:
    def __init__(self, data: Any, config: "RequestConfig"):
        self.data = data
        self.config = config

    def set_index(self, df: pd.DataFrame) -> pd.DataFrame:
        if "Tarih" in df.columns:
            df["Tarih_string"] = df["Tarih"]
            df.set_index("Tarih", inplace=True)
        return df

    def fix_column_names(self, df: pd.DataFrame):
        def fix(string: str):
            if "tarih" in string.lower() or "week" in string.lower():
                return string
            return string.replace("_", ".")

        df.columns = [fix(x) for x in df.columns]
        return df

    def _try_date(self, df: pd.DataFrame):
        if df.index.name is None:
            return df
        return try_date(df, frequency=self.config.frequency)

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
            df = self.set_index(df)
            df = self.fix_column_names(df)
            df = self._try_date(df)
        return df

    def __call__(self, *args, **kwargs) -> T_maybeDf:
        return self.process_to_dataframe()


def test_DataProcessor(capsys):
    with capsys.disabled():
        d = DataProcessor(False)
        print(d)
