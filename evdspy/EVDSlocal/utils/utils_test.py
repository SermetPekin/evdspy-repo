from pathlib import Path

import pandas as pd

from evdspy.EVDSlocal.index_requests.datagroups_initial import data_models_dict, data_strategy
from evdspy.EVDSlocal.index_requests.index_classes import GeneralIndexesDatagroups, GeneralIndexesDatagroupIndividual, \
    GeneralIndexesDatagroupSeriesList
from evdspy.EVDSlocal.index_requests.error_classes_index import ContentFunctionError
from evdspy.EVDSlocal.index_requests.df_operations import DFOperations
from evdspy.EVDSlocal.index_requests.index_util_funcs import json_to_excel, json_to_df, make_df_float
from ..common.files import Read
from ..common.table import Table2_
from ..components.api_params import DateStart, DateEnd
from ..components.options_class import SingletonOptions
from ..config.apikey_class import ApikeyClass
from ..config.config import ConfigBase
from ..initial.start_options import default_data_folder_name, Default_Prefix_
from ..requests_.ev_request import EVRequest
# import pytest


def get_api_key_while_testing():
    file_name = Path("..") / ".." / "api_key.txt"
    if not file_name.is_file():
        file_name = Path("..") / "api_key.txt"
    content = Read(file_name)
    lines = content.splitlines()
    line = tuple(line for line in lines if "evds" in line)
    api_key = line[0].split("=")[1]
    return str(api_key).strip()
