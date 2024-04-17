
import pandas as pd
from .datagroups_initial import data_models_dict, data_strategy
from .index_classes import GeneralIndexesDatagroups, GeneralIndexesDatagroupIndividual, \
    GeneralIndexesDatagroupSeriesList
from .error_classes_index import ContentFunctionError
from .df_operations import DFOperations
from .index_util_funcs import json_to_excel, json_to_df, make_df_float
from ..common.table import Table2_
from ..components.api_params import DateStart, DateEnd
from ..components.options_class import SingletonOptions
from ..config.apikey_class import ApikeyClass
from ..config.config import ConfigBase
from ..initial.start_options import default_data_folder_name, Default_Prefix_
from ..requests_.ev_request import EVRequest
config = ConfigBase()
# EVDSApiDomainDatagroupIndividual
def try_to_make_excel(json_content, file_name, try_float):
    try:
        json_to_excel(json_content, file_name, try_float=try_float)
        from ..common.colors import print_with_success_style
        print_with_success_style(f"{file_name} was created...")
    except:
        from ..common.colors import print_with_failure_style
        print_with_failure_style(f"{file_name} could not be created...")
def get_datagroup_individual_with_code(code_str: str):
    """get_datagroup_individual_with_code"""
    json_content = get_datagroup_individual_with_code_helper(code_str)
    # file_name = rf"SeriesData\EVPY_Data_{code_str}.xlsx"
    file_name = rf"{default_data_folder_name}\{Default_Prefix_}{code_str}.xlsx"
    if not json_content:
        return False
    if 'items' in json_content:
        json_content = json_content['items']
    try_to_make_excel(json_content, file_name, try_float=True)
    return json_content
def get_datagroup_individual_with_code_helper(
        code_str: str,
        start_date: str = None,
        end_date: str = None
):
    """get_datagroup_individual_with_code_helper"""
    gid = GeneralIndexesDatagroupIndividual(code=0, EVRequest_=EVRequest(
        options_=SingletonOptions()))  # this number will be overwritten . does not matter what number
    gid.create_url_first_part()
    gid.add_extra_params(code=code_str)
    if not start_date:
        start_date = SingletonOptions().get_valid_value("default_start_date")
    if not end_date:
        end_date = SingletonOptions().get_valid_value("default_end_date")
    date_start: DateStart = DateStart(value=start_date)
    date_end: DateEnd = DateEnd(value=end_date)
    gid.complete_url_instance.add_item(date_start)
    gid.complete_url_instance.add_item(date_end)
    gid.complete_url_instance.refresh_url()
    gid.complete_url_instance.add_apikey()  # this will get apikey itself if None given
    json_content = gid.get_json()
    return json_content
def get_series_list_of_subject(code_str: str):
    # https://evds2.tcmb.gov.tr/service/evds/serieList/key=XXXXX&type=csv&code=bie_yssk
    gid = GeneralIndexesDatagroupSeriesList(code=0, EVRequest_=EVRequest(
        options_=SingletonOptions()))  # this number will be overriten . does not matter what number
    gid.create_url_first_part()
    gid.add_extra_params(code=code_str)
    gid.complete_url_instance.refresh_url()
    json_content = gid.get_json()
    # file_name = rf"SeriesData\EVPY_Data_{code_str}_EXPLANATION.xlsx"
    file_name = rf"{default_data_folder_name}\{Default_Prefix_}{code_str}_EXPLANATION.xlsx"
    try_to_make_excel(json_content, file_name, try_float=False)
    return json_content
# ----------------------------------------------------------------------------------
""" Functions to return DF """
"""
    start_date = SingletonOptions().get_valid_value("default_start_date")
    end_date = SingletonOptions().get_valid_value("default_end_date")
"""
def get_df_datagroup(
        datagroup: str,
        start_date: str = None,
        end_date: str = None
):
    """returns all series as df to extend
        params:
        -----------------------
        datagroup : str
            e.g. `bie_yssk`
        start_date : str
            e.g. `31-01-2010`
        end_date : str
            e.g. `31-01-2030`
    """
    # https://evds2.tcmb.gov.tr/service/evds/datagroup=bie_yssk&startDate=01-06-2017&endDate=07-09-2017&type=csv&key=XXXX
    json_content = get_datagroup_individual_with_code_helper(datagroup, start_date, end_date)
    df = json_to_df(json_content)
    df = make_df_float(df)
    return df