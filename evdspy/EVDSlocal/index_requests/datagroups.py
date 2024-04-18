
import pandas as pd
from .datagroups_initial import data_models_dict, data_strategy
from .index_classes import GeneralIndexesDatagroups
from .error_classes_index import ContentFunctionError
from .df_operations import DFOperations
from ..common.table import Table2_
from ..components.options_class import SingletonOptions
from ..config.config import ConfigBase
from ..requests_.ev_request import EVRequest
config = ConfigBase()
# https://evds2.tcmb.gov.tr/service/evds/datagroup=bie_yssk&startDate=01-06-2017&endDate=07-09-2030&type=json&key=XXYYZZ
def get_datagroups_with_code(code=1):
    gid = GeneralIndexesDatagroups(code=code, EVRequest_=EVRequest(options_=SingletonOptions()))  #
    json_content = gid.get_json()
    return json_content
def get_keys() -> tuple:
    keys = ('DATAGROUP_CODE', 'DATAGROUP_NAME_ENG',
            'DATAGROUP_NAME', 'FREQUENCY',
            'DATASOURCE_ENG', 'FREQUENCY_STR',
            'START_DATE', 'END_DATE'
            )
    return keys
def get_title(item: dict) -> str:
    return item['DATAGROUP_NAME_ENG']
def get_value_from_datagroups_dict(item: dict, key: str) -> str:
    value = item.get(key, None)  # str(item[key])
    value = str(value)
    return value
import typing as t
def get_titles_and_ids_for_selection(json_content: dict) -> t.List[t.Tuple[str, str]]:
    new_list = []
    for item in json_content:
        title: str = get_value_from_datagroups_dict(item, 'DATAGROUP_NAME_ENG')
        code: str = get_value_from_datagroups_dict(item, 'DATAGROUP_CODE')
        new_list.append((code, title))
    return new_list
def show_datagroups_summary(json_content: dict) -> None:
    keys = get_keys()
    for item in json_content:
        new_list = []
        for key in keys:
            value = get_value_from_datagroups_dict(item, key)
            new_list.append((key, value,))
        title = get_title(item)
        Table2_().show(list_=new_list, title=title, columns=('key', 'value'), skiprow=0)
def json_to_df(json_content: list, code: int) -> None:
    df = pd.DataFrame.from_records(json_content)
    file_name = f"dataGroupOut-{code}.xlsx"
    try:
        df.to_excel(file_name)
    except:
        print(f"could not write excel file {file_name}. =>file is probably open")
        # data_model_type = data_models_dict['json']
    # process_datagroups(data_model_type, json_content)
def get_and_process_datagroups_with_code(code=1):
    json_content: dict = get_datagroups_with_code(code)
    show_datagroups_summary(json_content)
    return get_titles_and_ids_for_selection(json_content)
    # exit()
    # json_to_df(json_content, code)
def get_all_groups():
    # numbers = (1, 2, 3, 4, 5, 12, 13, 14, 15, 18, 19, 20, 21, 22, 23, 6, 7, 24, 25, 26, 27, 28, 95,)
    numbers = (18, 19,)
    for num in numbers:
        try:
            get_and_process_datagroups_with_code(num)
        except Exception as exc:
            print(exc)
            pass
import warnings
def get_datagroups() -> str:
    warnings.warn("get_datagroups will be removed in future version. Please use get_series istead [...]",
                  DeprecationWarning)
    return GeneralIndexesDatagroups(EVRequest_=EVRequest(options_=SingletonOptions())).create_url()
# def process_datagroups(data_model_type, content):
#     df_op = DFOperations(data_model_type(data=content))
#     df_op.convert_to_df_abstract()
#     df = pd.DataFrame.from_records(content)
#     df.to_excel("t123.xlsx")