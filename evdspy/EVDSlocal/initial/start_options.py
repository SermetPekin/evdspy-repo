""" S T A R T   O P T I O N S """
#
#
#   see SingletonOptions.py
#
from ..common.common_imports import *
from pathlib import Path


def check_if_this_is_pytest():
    def check():
        path_ = Path(sys.argv[0])
        return "pytest" in str(path_.stem)

    if len(sys.argv) > 0 and check():
        return True
    else:

        return False

#
#
#
if True:
    default_series_file_name = "config_series.cfg"
    default_data_folder_name = "SeriesData"
    Avoid_Absolute_Paths_ = True
    Default_Prefix_ = "EVPY_"
    # options_folder_name = r"IO"
    DEBUG_LOG_CANCEL = False
    DEGUB_NOTICE = True
    DEBUG_PRINT = False
    default_arch_folder_name = "APIKEY_FOLDER"
    default_arch_file_name = "arch.txt"
    default_cache = "daily"  # nocache / hourly / monthly
    default_end_date = "01-12-2030"
    default_start_date = "01-01-2019"
    import os

    # USERNAME = os.getenv("USERNAME")  # or hard coded "Username"
#
#
#
#
#
#
#
#
#
#
""" / S T A R T   O P T I O N S """

# pytest will set this True
current_mode_is_test = check_if_this_is_pytest()

""" GLOBALS """
