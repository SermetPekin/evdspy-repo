# ------------------------------------------------------------------------------
from ..common.files import *
from dataclasses import dataclass
from .series_examples import *
from ..components.evds_seri_files import EvdsSeriesRequestWrapper, EvdsSeriesRequest, EvdsSeri
from evdspy.EVDSlocal.series_format.populate_series import *
from evdspy.EVDSlocal.config.config import default_series_file_name

import random
from ..common.colors import *

GSEP = "--"

# ------------------------------------------v1.0 refactored------------------------------------------------------
from pathlib import Path


def get_approval(file_name):
    msg = f"{file_name} already exists. \n If you would like to replace it with a new example please type `replace`: "
    print_get_input_style(msg )
    ans = input()
    if str(ans).lower().strip() == "replace":
        return True
    return False


def create_series_text_file(file_name: str, content=""):
    """General usage"""
    if Path(file_name).is_file() and "-locked" not in file_name.lower():
        if not get_approval(file_name):
            return False
    print_with_creating_style(f"creating...{file_name}")
    result, msg = Write(file_name, content)
    print_with_success_style(msg)
    time.sleep(1)
    return result


def create_series_text_example(file_name: str = default_series_file_name, onsetup: bool = False):
    if onsetup:
        if file_exists_show_and_return(file_name):
            return
    """ main series config file """
    return create_series_text_file(file_name, random.choice(example_series))


# ------------------------------------------ / v1.0 refactored------------------------------------------------------


def series_file_info(file_name):
    print_with_info_style(f"In order to use your own choice of data series in "
                          f"`{file_name}` you may change this file accordingly")


from evdspy.EVDSlocal.components.bucket_from_series import BucketFromSeriesFile


def get_locked_file_title():
    title = f"""
#package : evdspy
#author  : sermet.pekin
#Series_config_file_LOCKED :Please do not modify.
#
#						E V D S P Y  _  C O N F I G  _  F I L E (LOCKED) ---------------------------------------------
#	
# 	-----------------------------------------------------------------------------------------
#		NOTE : PLEASE DO NOT MODIFY *LOCKED* VERSION OF THE CONFIG FILE (THIS FILE). 
#       BECAUSE IT WILL NOT HAVE EFFECT ON RUN.
#       INSTEAD IF YOU WOULD LIKE TO MODIFY ANY PROPERTIES OF SERIES OR OTHER OPTIONS
#       YOU MAY MODIFY UNLOCKED VERSION OF THIS FILE. (`config_series.cfg`)
#		    
#       THIS FILE(LOCKED) IS HELP USERS TO SEE HOW MACHINE MODIFIED DEFAULT OPTIONS 
#       DURING RUN AFTER CHECKING PROCESS.
#		 
# -------------------------------------------------------------------------------------------


"""
    return title


from evdspy.EVDSlocal.setup_project.user_series_config import frequency_dict, formulas_dict
from evdspy.EVDSlocal.state.current_state import CurrentState
from typing import Dict
from evdspy.EVDSlocal.components.request_or_cache import RequestOrCacheResultInfo


def get_request_results():
    result_data_dict: Dict[str, RequestOrCacheResultInfo] = CurrentState().get_result_dict()
    items = result_data_dict.items()
    items_str_list = (tuple_request_or_cache_info[1].get_data() for tuple_request_or_cache_info in items)

    result_content = "\n".join(items_str_list)
    result = f"""
------------REQUEST or CACHE RESULTS------------------
{result_content}
------------/REQUEST or CACHE RESULTS------------------
"""
    return result


def create_content(bfs: BucketFromSeriesFile, evds_series_request_: EvdsSeriesRequest, subject,
                   series_list: List[EvdsSeri]):
    list_ = [x.ID for x in series_list]
    series_list_str = "\n".join(list_)
    r = f"""
---Series---------------------------------
foldername : {bfs.folder_name}
abs_path : {bfs.abs_path}
subject  : {subject}
prefix   : {bfs.prefix}
frequency : {bfs.frequency}                # {frequency_dict.get(int(bfs.frequency), 'Not Found (request will be made with default option for this property)')}
formulas : {bfs.formulas}                  # {formulas_dict.get(int(bfs.formulas), 'Not Found (request will be made with default option for this property)')}
aggregateType : {bfs.aggregateType} 

------------SERIES CODES------------------
{series_list_str}
------------/SERIES CODES------------------



---/Series---------------------------------
--++--
"""
    return r


def create_series_file_from_Wrapper(wrapperList: List[EvdsSeriesRequestWrapper]):
    contents = []
    for EvdsSeriesRequestWrapper_ in wrapperList:
        name = EvdsSeriesRequestWrapper_.name
        subject = EvdsSeriesRequestWrapper_.subject
        series_list = EvdsSeriesRequestWrapper_.EvdsSeriesRequest_.series_list
        contents.append(
                create_content(EvdsSeriesRequestWrapper_.bfs, EvdsSeriesRequestWrapper_.EvdsSeriesRequest_, subject,
                               series_list))
    cont = get_locked_file_title() \
           + f"\n{GSEP}".join(contents) \
           + get_request_results()

    return cont


from ..components.evds_seri_files import *


# ------------------------------------------------------------------------------
# /*
#               SeriesFileFormat
#
# ------------------------------------------------------------------------------
# */

@dataclass
class SeriesFileFormat:
    series_filename: str
    EvdsSeriesRequestWrapperList: any = None

    def __post_init__(self):
        self.get_series_from_file()

    def read(self):
        return Read(self.series_filename, f"{self.series_filename} problem")

    def get_series_from_file(self):
        self.EvdsSeriesRequestWrapperList: \
            List[EvdsSeriesRequestWrapper] = \
            PopulateSeries(
                    self.series_filename
            ).split_series_file()
        return self.EvdsSeriesRequestWrapperList



def test_SeriesFileFormat2():
    sff = SeriesFileFormat("series.txt")
    return sff.EvdsSeriesRequestWrapperList  # s.read()


# ------------------------------------------------------------------------------
# /*
#               SeriesCreator
#
# ------------------------------------------------------------------------------
# */
@dataclass
class SeriesCreator:

    def create(self):
        ...
