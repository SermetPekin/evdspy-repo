
""" S T A R T   O P T I O N S """
#
#
#   see SingletonOptions.py
#
from ..common.common_imports import *
from pathlib import Path
import sys
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
    """temporarily cancel mock requests and do real requests"""
    temp_cancel_mock_request = True
    """series file name """
    default_series_file_name = "config_series.cfg"
    """series data folder name """
    default_data_folder_name = "SeriesData"
    """ for security as a default value it is True to avoid polluting existing folders with unwanted excel files """
    Avoid_Absolute_Paths_ = True
    """ for security we define a prefix to name created excel files to diminish risk of removing existing excel files """
    Default_Prefix_ = "EVPY_"
    # options_folder_name = r"IO"
    """ debug option """
    DEBUG_LOG_CANCEL = False
    """ debug notice """
    DEGUB_NOTICE = True
    """verbose debug """
    DEBUG_PRINT = False  # TODO less verbose debug plus conditional
    """ api key tested hashes folder name  """
    default_arch_folder_name = "APIKEY_FOLDER"
    """ api key tested hashes file name  """
    default_arch_file_name = "arch.txt"
    """default_cache"""
    default_cache = "daily"  # nocache / hourly / monthly
    """default_end_date"""
    default_end_date = "01-12-2030"
    """default_start_date"""
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