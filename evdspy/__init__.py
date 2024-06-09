# ------------------------------------------------------
#
#       __init__
#                           package: evdspy @2022
# ------------------------------------------------------
from evdspy.EVDSlocal.main_ import *
from evdspy.EVDSlocal.index_requests.get_series_indexes import (

    get_series,
)

from evdspy.EVDSlocal.utils.utils_general import ls

from evdspy.EVDSlocal.index_requests.get_series_indexes_utils import (
    default_start_date_fnc,
    default_end_date_fnc,
    correct_types,
)



# __all__ = [

#         "default_start_date_fnc",
#         "default_end_date_fnc",
#         "correct_types",
#         "get_series" ,
#         "ls"
#     'easy_setup',
#     'setup',
#     'setup_series',
#     "setup_series_steps",
#     'help_evds',
#     'check',
#     'get',
#     'h',
#     'help_evdspy',
#     'help_',
#     'create_series_file',
#     'csf',
#     'show',
#     'get_df_test',
#     'console',
#     'menu',
#     'menu_onload',
#     'version',
#     'save_apikey',
#     'save',
#     'remove_cache',
#     'create_options_file',
#     'cof',
#     'console_main',
#     'get_df_datagroup',
#     'get_datagroups_with_code',
#     'get_category_name' ,
#     'get_series_list_of_subject'
# ]