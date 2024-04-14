from rich import inspect

from .datagroups_initial import data_models_dict , data_strategy , GID_json , GID_csv
from .index_classes import  GeneralIndexesDatagroups
from .error_classes_index import ContentFunctionError
from .df_operations import DFOperations
from evdspy.EVDSlocal.common.files import Write, Read
import typing as t
import json
from .datagroups import get_datagroups_df


def get_datagroups_data(data_strategy_type="json"):
    # csv = GeneralIndexesDatagroups().get_csv()
    buffer_function: t.Callable = data_strategy[data_strategy_type]  # GeneralIndexesDatagroups().get_json
    content_fn: t.Callable = buffer_function(1)
    content: str | t.Callable = content_fn()
    if callable(content):
        # inspect(content, all=True)
        content = content()
        # raise "content"
    if content:
        inspect(content, all=True)
        if isinstance(content, tuple([list, tuple])):
            # content = "\n".join(content)
            content = json.dumps(content)
        Write("subject_list.txt", content)
    else:
        inspect(content)
    get_datagroups_df(data_strategy_type, content)
    return content