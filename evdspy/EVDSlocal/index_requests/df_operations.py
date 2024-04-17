
import time
import pandas as pd
from ..components.evds_files import DfColumnsDoesNotMatch
from ..config.config import config
from ..common.colors import print_with_failure_style, print_with_updating_style, print_with_info_style
from .data_models import *
from dataclasses import dataclass
@dataclass
class DFOperations():
    data_model: DataModel
    df: pd.DataFrame = None
    @staticmethod
    def extract_values_from_line(line: str, sep=","):
        return line.split(sep)
    @staticmethod
    def line_gen(buffer: str):
        if not buffer:
            return False
        for item in buffer.split("\n"):
            yield item
    def get_columns_from_first_row(self):
        first_row = self.data_model.data.split("\n")[0].split(",")
        return first_row
    def get_columns(self, df):
        current_columns = df.columns  # rangeIndex
        if isinstance(current_columns, pd.RangeIndex):
            current_columns_len = len([x for x in current_columns])
        else:
            current_columns_len = len(current_columns)
        potential_columns = self.get_columns_from_first_row()
        if len(potential_columns) != current_columns_len:
            raise DfColumnsDoesNotMatch()
        df.columns = self.get_columns_from_first_row()
        UnixTime = 'UNIXTIME'
        if UnixTime in df.columns:
            df.drop(UnixTime, axis=1, inplace=True)
        if config.current_mode_is_test:
            ...
            # self.save_excel("testpytest2.xlsx")
        return df
    def save_excel(self, name):
        if isinstance(self.df, pd.DataFrame):
            self.df.to_excel(name)
    @staticmethod
    def list_to_df(items):
        return pd.DataFrame(items)
    def make_df_float(self):
        def check_cols(x: str):
            items = (
                "Tarih" not in x,
                "WEEK" not in x,
                "DAY" not in x,
            )
            return all(items)
        columns = (x for x in self.df.columns if check_cols(x))
        other_cols = (x for x in self.df.columns if not check_cols(x))
        old_df = self.df
        try:
            self.df = self.df[columns].astype(float)
        except:
            print_with_failure_style("Could not convert some columns to float type...")
        for other_column in other_cols:
            self.df[other_column] = old_df[other_column]
    def convert_to_df_abstract(self):
        from rich import inspect
        inspect(self.data_model)
        obj = {
            "csv": self.convert_csv_df,
            "json": self.convert_json__df
        }
        fn = obj[self.data_model.type_name]
        fn()
    def convert_json__df(self, json_buffer: str = None):
        # print("To be implemented soon...")
        print(json_buffer)
        exit()
        # raise NotImplementedError
    def convert_csv_df(self, csv_buffer: str = None):
        if csv_buffer is None:
            csv_buffer = self.data_model.data
        pd_rows = list(
            map(self.extract_values_from_line,
                (item for item in self.line_gen(csv_buffer))
                )
        )
        if not pd_rows:
            # print("convert_csv_df get empty buffer ")
            return
        pd_rows.pop(0)
        self.df_no_columns = self.list_to_df(pd_rows)
        try:
            self.df = self.get_columns(self.df_no_columns)
        except DfColumnsDoesNotMatch:
            print_with_failure_style("columns did not match returning df with no columns...")
            self.df = self.df_no_columns
            print(self.df.head())
            # filename = "error_" + str(id(self.df)) + ".xlsx"
            # print_with_updating_style("file was saved", filename)
            # self.df.to_excel(filename)
            print_with_info_style("This error will be checked again...")
            time.sleep(1)
            return False
        except Exception as e:
            print_with_failure_style(e)
            pass
        self.make_df_float()
        return self.df