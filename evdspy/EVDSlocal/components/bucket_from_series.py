
from ..common.common_imports import *
from ..common.files import *
from dataclasses import dataclass
import os
from pathlib import Path
from evdspy.EVDSlocal.messages.error_classes import BucketFromSeriesFolderCreateError
from evdspy.EVDSlocal.config.config import *
from ..initial.start_args import Args
from ..components.options_class import Options, load_options, SingletonOptions
from evdspy.EVDSlocal.initial.start_options import default_data_folder_name
from evdspy.EVDSlocal.common.folder_name_checks import check_remove_back_slash
from dataclasses import dataclass
import os
from pathlib import Path
from evdspy.EVDSlocal.components.api_params import FrequencyEnum, Frequency, AggregationEnum, Aggregations, \
    get_enum_with_value, FormulasEnum, Formulas
# ------------------------------------------------------------------------------
# /*
#               BucketFromSeriesFile
#
# ------------------------------------------------------------------------------
# */
from evdspy.EVDSlocal.components.request_or_cache import RequestOrCacheResultInfo
@dataclass
class BucketFromSeriesFile:
    folder_name: any
    subject: str
    frequency: str
    formulas: str
    aggregateType: str
    prefix: str = Default_Prefix_
    NullType: bool = False
    abs_path: any = None
    xls_name_path: str = "test"
    request_or_cache_resultInfo_: field(default_factory=RequestOrCacheResultInfo) = False
    def __post_init__(self):
        """ Check 2 => after writing avoid \foldername\foldername instead of foldername\foldername
            we previously checked while getting input from user but
            we are checking if user added any absolute path by mistake
        """
        def get_defaults(item, default_value):
            if item == "":
                return default_value
            return item
        # self.frequency = get_defaults(str(self.frequency), default_freq)
        # self.formulas = get_defaults(self.formulas, default_formulas_)
        # self.aggregateType = get_defaults(self.aggregateType, default_AggregateType_)
        from evdspy.EVDSlocal.setup_project.user_series_config import default_freq, default_formulas_, \
            default_AggregateType_
        self.frequency: str = get_defaults(str(self.frequency), default_freq)
        self.frequency = get_enum_with_value(self.frequency, FrequencyEnum, FrequencyEnum.default)
        self.formulas: str = get_defaults(self.formulas, default_formulas_)
        self.formulas: str = get_enum_with_value(self.formulas, FormulasEnum, FormulasEnum.default)
        self.aggregateType = get_defaults(self.aggregateType, default_AggregateType_)
        self.aggregateType: str = get_enum_with_value(self.aggregateType, AggregationEnum, AggregationEnum.default)
        self.folder_name = check_remove_back_slash(self.folder_name)
        self.abs_path = self.get_folder_name(self.folder_name)
        self.xls_name_path = str(Path(self.abs_path) / (self.prefix + '_' + self.subject))
    def __str__(self):
        s = f"""
frequency : {self.frequency}
formulas : {self.formulas}
aggregateType : {self.aggregateType}
folder_name : {self.folder_name}
abs_path : {self.abs_path}
xls_name_path : {self.xls_name_path}
"""
        return s
    def get_folder_name(self, folder_name: str):
        def adapt_folder_name(relative_folder, reduce=False):
            if reduce:
                relative_folder = Path(folder_name).stem
            abs_modified = Path() / default_data_folder_name / relative_folder
            return abs_modified
        if folder_name is None:
            return ""
        if Avoid_Absolute_Paths_ and SingletonOptions().options_.avoid_absolute_paths_user:
            """ Namespace Protection is on """
            r"""
            This is extra protection to prevent mismatching of unwanted paths and populating some files replacing
            old files, if the user is sure absolute paths are correct they can modify
                Avoid_Absolute_Paths_ variable in start_options.py file
                avoids : C:Users\Userx\XdataFolderName
                changes paths to correct form : ...WorkingDirectory..\SeriesData\XdataFolderName
            """
            reduce = False
            if Path(folder_name).is_absolute():
                reduce = True
            return adapt_folder_name(folder_name, reduce=reduce)
        """ Namespace Protection turned off by user """
        print("Avoid_Absolute_Paths_ was cancelled")
        if self.create_folder():
            """ now we will return absolute path if we can successfully create the folder"""
            return self.abs_path
        return adapt_folder_name(self.abs_path, reduce=True)
    def create_folder(self):
        if is_dir(self.abs_path):
            return True
        try:
            os.makedirs(self.abs_path)
            return True
        except:
            if not config.current_mode_is_test:
                print(f"could not create folder {self.abs_path} ")
                # raise BucketFromSeriesFolderCreateError
            return False
from evdspy.EVDSlocal.setup_project.user_series_config import default_freq, default_formulas_, \
    default_AggregateType_
null_BucketFromSeriesFile = BucketFromSeriesFile(folder_name=None,
                                                 subject="test",
                                                 frequency=default_freq,
                                                 formulas=default_formulas_,
                                                 aggregateType=default_AggregateType_,
                                                 prefix="EV_",
                                                 NullType=True)