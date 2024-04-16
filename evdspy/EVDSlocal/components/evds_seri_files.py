
from ..common.common_imports import *
from ..common.files import *
from dataclasses import dataclass
import os
from pathlib import Path
from evdspy.EVDSlocal.messages.error_classes import BucketFromSeriesFolderCreateError
from evdspy.EVDSlocal.config.config import *
from ..config.apikey_class import ApikeyClass
from ..initial.start_args import Args
from ..components.options_class import Options, load_options, SingletonOptions, read_user_options_on_load
from evdspy.EVDSlocal.initial.start_options import default_data_folder_name, Default_Prefix_
from evdspy.EVDSlocal.components.bucket_from_series import BucketFromSeriesFile, null_BucketFromSeriesFile
from evdspy.EVDSlocal.components.url_class import URLClass
from evdspy.EVDSlocal.components.api_params import Series, DateStart, DateEnd, dataTypeParam, dataTypeEnum
from typing import Tuple, Union, List
from rich import inspect
# ------------------------------------------------------------------------------
# -------------------------------------------------EvdsSeri----------------------
@dataclass
class EvdsSeri:
    """
    EvdsSeri
    """
    ID: str
    bfs: BucketFromSeriesFile
    name: str = ""
    subject: str = ""
    def __repr__(self):
        content = f"""
        <EvdsSeri>
            ID : {self.ID}
            name : {self.name}
            subject : {self.subject}
            bfs : {self.bfs}
        </EvdsSeri>
"""
        # print(content)
        return content
#   ----------------------------------------------------------    / EvdsSeri
liste = ('TP.IHRACATBEC.9999', 'TP.IHRACATBEC.31', 'TP.IHRACATBEC.41')
seri_evds_test_objs = tuple(EvdsSeri(x, bfs=null_BucketFromSeriesFile) for x in liste)
# ------------------------------------------------------------------------------
# /*
#               EvdsSeriesRequest
#
# ------------------------------------------------------------------------------
# */
@dataclass
class EvdsSeriesRequest:
    bfs: BucketFromSeriesFile
    options_: Optional[Options] = load_options()
    # series_list: field(default_factory=list) = field(default_factory=list[seri_evds_test_objs])
    series_list: field(default_factory=list) = tuple(seri_evds_test_objs)
    complete_url_instance: URLClass = None
    def __post_init__(self):
        read_user_options_on_load()
        self.start_date: str = SingletonOptions().get_valid_value("default_start_date")
        self.end_date: str = SingletonOptions().get_valid_value("default_end_date")
        self.update_url_instance()
    def update_url_instance(self):
        """_summary_
        update_url_instance
        """
        date_start: DateStart = DateStart(value=self.start_date)
        date_end: DateEnd = DateEnd(value=self.end_date)
        type_param = dataTypeParam(value=dataTypeEnum.csv)
        slist: Tuple[str] = tuple(x.ID for x in self.series_list)
        series_instance = Series(slist)
        full_list = [series_instance, date_start, date_end, type_param]
        complete_url_instance = URLClass(full_list)
        number_of_series = len(slist)
        # ADD other params from file
        complete_url_instance.add_formulas(self.bfs.formulas, number_of_series)
        complete_url_instance.add_frequency(self.bfs.frequency)
        complete_url_instance.add_aggtype(self.bfs.aggregateType, number_of_series)
        api_key = ApikeyClass().get_valid_api_key()
        complete_url_instance.add_apikey(api_key)
        self.complete_url_instance = URLClass(complete_url_instance.url_items)
        self.complete_url_instance.refresh_url()
        self.complete_url_instance.create_report()
#   ----------------------------------------------------------    / EvdsSeriesRequest
test_series_ = EvdsSeriesRequest(options_=load_options(), series_list=seri_evds_test_objs,
                                 bfs=null_BucketFromSeriesFile)
# ------------------------------------------------------------------------------
# /*
#               EvdsSeriesRequestWrapper(s)
#
# ------------------------------------------------------------------------------
# */
from abc import ABC, abstractmethod
@dataclass
class EvdsSeriesRequestWrapper():
    name: str
    subject: str
    EvdsSeriesRequest_: EvdsSeriesRequest
    bfs: BucketFromSeriesFile = None  # field(default=null_BucketFromSeriesFile)
    # bfs: BucketFromSeriesFile = null_BucketFromSeriesFile
    def __post_init__(self):
        self.EvdsSeriesRequest_.bfs = self.bfs
def EvdsSeriesRequestWrapperBasic(name: str, subject: str, EvdsSeriesRequest_: EvdsSeriesRequest):
    bfs = BucketFromSeriesFile(name, subject, prefix=Default_Prefix_)
    return EvdsSeriesRequestWrapper(name, subject, EvdsSeriesRequest_, bfs)
def EvdsSeriesRequestWrapperFromFile(bfs: BucketFromSeriesFile, EvdsSeriesRequest_: EvdsSeriesRequest):
    return EvdsSeriesRequestWrapper(bfs.subject, bfs.subject, EvdsSeriesRequest_, bfs)
#   ----------------------------------------------------------    / EvdsSeriesRequestWrapper
__all__ = [
    'EvdsSeriesRequest',
    'test_series_',
    'EvdsSeri',
    'EvdsSeriesRequestWrapper',
    'EvdsSeriesRequestWrapperFromFile',
    'EvdsSeriesRequestWrapperBasic',
]