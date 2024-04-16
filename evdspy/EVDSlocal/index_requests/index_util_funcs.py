
import pandas as pd
import typing as t
from ..common.colors import print_with_failure_style
from ..components.excel_class import correct_folder
def make_date_first_column_helper(df, col_name):
    if not col_name in df.columns:
        return df
    cols = [col_name] + [col for col in df if col != col_name]
    df = df[cols]
    return df
def make_date_first_column(df):
    col_names = ('YEARWEEK', 'Tarih',)
    for col_name in col_names:
        df = make_date_first_column_helper(df, col_name)
    return df
def drop_unix(df):
    UnixTime = 'UNIXTIME'
    if UnixTime in df.columns:
        df.drop(UnixTime, axis=1, inplace=True)
    return df
def json_to_df(json_content: t.Union[list, dict]):
    if hasattr(json_content, 'items'):
        json_content = json_content['items']
    df = pd.DataFrame.from_records(json_content)
    df = drop_unix(df)
    df = make_date_first_column(df)
    return df
def make_df_float(df):
    def check_cols(x: str):
        items = (
            "Tarih" not in x,
            "WEEK" not in x,
            "DAY" not in x,
            "YEAR" not in x,
        )
        return all(items)
    columns = (x for x in df.columns if check_cols(x))
    other_cols = (x for x in df.columns if not check_cols(x))
    old_df = df
    try:
        df = df[columns].astype(float)
    except:
        print_with_failure_style("Could not convert some columns to float type...")
    for other_column in other_cols:
        df[other_column] = old_df[other_column]
    return df
def json_to_excel(json_content: list, file_name, try_float=True):
    file_name = correct_folder(file_name, "xlsx")
    df = json_to_df(json_content)
    if try_float:
        df = make_df_float(df)
    try:
        df = make_date_first_column(df)
        df.to_excel(file_name)
    except:
        print(f"could not write excel file {file_name}. =>file is probably open")