import json
import time
import pandas as pd
from .index_classes import GeneralIndexesDatagroups
from evdspy.EVDSlocal.common.files import Write, Read
from ..components.evds_files import DfColumnsDoesNotMatch
from ..config.config import config
from ..common.colors import print_with_failure_style, print_with_updating_style, print_with_info_style
from dataclasses import dataclass
from abc import ABC
from dataclasses import dataclass
from .data_models import DataModel, DataModelCSV, DataModelJSON
from .df_operations import DFOperations

from abc import ABC
from dataclasses import dataclass


def get_datagroups() -> str:
    return GeneralIndexesDatagroups().create_url()


GID_csv = lambda x: GeneralIndexesDatagroups().get_csv
GID_json = lambda x: GeneralIndexesDatagroups().get_json

data_strategy = {"csv": GID_csv, "json": GID_json}
data_models_dict = {"csv": DataModelCSV, "json": DataModelJSON}

from rich import inspect


def get_datagroups_data(data_strategy_type="json"):
    # csv = GeneralIndexesDatagroups().get_csv()
    buffer_function = data_strategy[data_strategy_type]
    content_fn = buffer_function(1)
    content = content_fn()
    if callable(content):
        # inspect(content, all=True)
        content = content()
        # raise "content"
    if content:
        inspect(content, all=True)
        if isinstance(content, tuple([list, tuple])):
            # content = "\n".join(content)
            content = json.dumps( content )
        Write("subject_list.txt", content)
    else:
        inspect(content)
    get_datagroups_df(data_strategy_type, content)
    return content


class ContentFunctionError(BaseException):
    """ContentFunctionError this
        this one happens when strategy function is not Callable
    """


def get_datagroups_df(data_model_type_key="csv", content=None):
    if content is None:
        """fn () """

        content_fn = data_strategy.get(data_model_type_key, None)
        if callable(content_fn):
            content = content_fn()
        else:
            raise ContentFunctionError()

    data_model_type = data_models_dict[data_model_type_key]
    df_op = DFOperations(data_model_type(data=content))
    df_op.convert_to_df_abstract()
    # df_op.save_excel("test1.xlsx")
