# from ..common.common_imports import *
import time
from dataclasses import dataclass
from collections import namedtuple
from typing import Callable, List, Tuple, Union
from ..common.colors import *

from evdspy.EVDSlocal.components.options_class import SingletonOptions
from evdspy.EVDSlocal.config.config import *
from evdspy.EVDSlocal.common.files import *
from evdspy.EVDSlocal.setup_project.user_series_config import *
from evdspy.EVDSlocal.setup_project.user_series_config import formulas_dict, frequency_dict
from evdspy.EVDSlocal.setup_project.user_setup_helper import series_title
from evdspy.EVDSlocal.setup_project.user_options_config import items_from_user_config, \
    explanations_config, default_answers_config, check_funcs_options, transform_answers_options

from evdspy.EVDSlocal.config.config import config
from evdspy.EVDSlocal.initial.start_options import default_cache, default_end_date, default_start_date

# ----------------------------------------------------SetupInputs---------------------------

# -----------------------------------------------------------------------------------------
# SetupInputsConfig = namedtuple('SetupInputsConfig', 'cache_freq gl_date_start gl_date_end')
# SetupInputsSeries = namedtuple('SetupInputsSeries',
#                                'data_folder subject prefix ecodes frequency formulas aggregateType')

cache_freq = SingletonOptions().options_.default_cache
gl_date_start = SingletonOptions().options_.default_start_date
gl_date_end = SingletonOptions().options_.default_end_date
avoid_absolute_paths = SingletonOptions().options_.avoid_absolute_paths


@dataclass
class SetupInputsConfig:
    cache_freq: str = SingletonOptions().options_.default_cache
    gl_date_start: str = SingletonOptions().options_.default_start_date
    gl_date_end: str = SingletonOptions().options_.default_end_date
    avoid_absolute_paths: str = SingletonOptions().options_.avoid_absolute_paths


@dataclass
class SetupInputsSeries:
    data_folder: str
    subject: str
    prefix: str
    ecodes: tuple
    frequency: str
    formulas: str
    aggregateType: str


# -----------------------------------------------------------------------------------------


from enum import Enum


# ----------------------------------------------------configType---------------------------
class configType(Enum):
    Series = 1
    Config = 2


# ----------------------------------------------------InputItem----------------------

@dataclass
class InputItem:
    msg: str
    long_msg: str = ""
    check_func: Callable = TrueFunc
    transform_func: Callable = same
    optional: bool = True

    # -----------------------------------------------------------------------------------------


"""
            GetInputFromUser
"""

# -----------------------------------------------------------------------------------------
from abc import ABC, abstractmethod


# ----------------------------------------------------GetInputFromUser----------------------
@dataclass
class GetInputFromUser(ABC):
    items: List[InputItem]
    config_type: configType

    @abstractmethod
    def ask_user(self, msg, check_func):
        pass

    @abstractmethod
    def get_from_user(self, item, explanation, check_func):
        pass

    @abstractmethod
    def process(self):
        pass


@dataclass
class GetInputFromUserBase():
    items: List[InputItem]
    config_type: configType

    def ask_user(self, msg, check_func):
        ans = input(msg)
        if not check_func(ans):
            return self.ask_user(msg, check_func)
        return ans

    def get_from_user(self, item, explanation, check_func):
        window = f"*" * 50 + "\n"
        msg = f"{window}**{item} \n {explanation} :"
        if config.current_mode_is_test:
            return 'pytest running'
        # ans = input(msg)
        ans = self.ask_user(msg, check_func)
        if not ans.strip():
            msg = "==> Continued with default value ..."
            print_with_updating_style(msg)
        print_with_creating_style(f"{window}")
        return str(ans)

    def process(self):
        assert config.current_mode_is_test is False, "config.current_mode_is_test is False"
        if config.current_mode_is_test:
            return get_default_setup_answers(self.config_type)
        user_typed: List = []
        for item in self.items:
            ans = self.get_from_user(item.msg, item.long_msg, item.check_func)
            """ We will transform users answer same / split for now """
            ans = item.transform_func(ans)

            user_typed.append(ans)

        # user_typed = list(map(lambda x: x , user_typed))
        self.user_typed = user_typed
        return tuple(user_typed)


# ----------------------------------------------------GetInputFromUserConfig----------------------
@dataclass
class GetInputFromUserConfig(GetInputFromUserBase):
    """  GetInputFromUserConfig  """
    items: List[InputItem]
    config_type: configType = configType.Config


# ----------------------------------------------------GetInputFromUserSeries----------------------
@dataclass
class GetInputFromUserSeries(GetInputFromUserBase):
    """  GetInputFromUserSeries  """
    items: List[InputItem]
    config_type: configType = configType.Series


# ----------------------------------------------------create_Input_Items----------------------
def create_Input_Items(
        config_type: configType,
        items_from_user: List, explanations: List,
        check_funcs: List[Callable],
        transform_answers: List[Callable],

):
    items: List[InputItem] = []
    for msg, explanation, check_func, transform_func in zip(items_from_user, explanations, check_funcs,
                                                            transform_answers):
        items.append(
            InputItem(
                msg=msg,
                long_msg=explanation,
                check_func=check_func,
                transform_func=transform_func
            )
        )

    GetInputFromUserClassType = {
        configType.Series: GetInputFromUserSeries,
        configType.Config: GetInputFromUserConfig
    }[config_type]

    GIF = GetInputFromUserClassType(
        items=items, config_type=config_type
    )
    return GIF.process()


from evdspy.EVDSlocal.components.evds_seri_files import EvdsSeri

from typing import List

from evdspy.EVDSlocal.common.folder_name_checks import check_remove_back_slash


# -------------- GOES to Utils  ------------------------
# split_items: any = lambda text : list(
#         text.translate(text.maketrans({x: "-" for x in "[,-/\n;]~"})).split("-"))
def split_items_multi(series_list: Union[str, List, Tuple]) -> str:
    """ 1.1 """

    def split_items(series_list) -> tuple:
        if isinstance(series_list, tuple([list, tuple])):
            return series_list
        return tuple(series_list.translate(series_list.maketrans({x: "-" for x in "[,-/\n;]~"})).split("-"))

    """ 1 """
    if isinstance(series_list, str):
        if not series_list.strip():
            series_list: list = default_answers_series
        else:
            series_list: list = list(split_items(series_list))
    if isinstance(series_list, tuple([list, tuple])):
        series_list_str: str = "\n".join(series_list)
    else:
        series_list_str: str = "\n".join(list(split_items(series_list)))

    return series_list_str


# -------------- GOES to Utils  ------------------------

def content_from_SetupInputsSeries(SI: SetupInputsSeries):
    """ S E R I E S """
    """
    namedtuple('SetupInputsSeries', 'data_folder subject prefix ecodes frequency formulas aggregateType')

    """

    def create_content(folder, subject, prefix, series_list: Union[Tuple, List, str]):
        folder_path = check_remove_back_slash(folder)
        # folder_path_series = str(Path().absolute() / folder / 'series.txt')
        abs_path = str(Path().absolute() / folder_path)

        series_list_str: str = split_items_multi(series_list)

        r = f"""{mainSepBegin}
foldername : {folder_path}
abs_path : {abs_path} # will check again before saving requests from the server it may be replaced by ...WD.../DataSeries/{folder_path}
subject  : {subject}
prefix   : {prefix}
frequency : {SI.frequency} # {frequency_dict[int(SI.frequency)]}
formulas : {SI.formulas} # {formulas_dict[int(SI.formulas)]}
aggregateType : {SI.aggregateType}
------------SERIES CODES------------------
{series_list_str}
------------/SERIES CODES------------------
{mainSepEnd}
{GSEP}"""
        return r

    return create_content(SI.data_folder, SI.subject, SI.prefix, tuple(SI.ecodes))


def content_from_SetupInputsOptions(SI: SetupInputsConfig):
    """ O P T I O N S  """
    """
    SetupInputsConfig = namedtuple('SetupInputsConfig', 'cache_freq gl_date_start gl_date_end')
    """

    def get_default(item):
        # SingletonOptions().get_valid_value("default_cache")
        # SingletonOptions().get_valid_value("default_start_date")
        # SingletonOptions().get_valid_value("default_end_date")

        cache_freq = SingletonOptions().options_.default_cache
        gl_date_start = SingletonOptions().options_.default_start_date
        gl_date_end = SingletonOptions().options_.default_end_date
        avoid_absolute_paths = SingletonOptions().options_.avoid_absolute_paths

        # result = SI.__getattribute__(item)
        # result = SI.__dict__.get(item, None)
        result = getattr(SI, item, None)
        if not result:
            result = locals()[item]
        return result

    def create_content():
        cache_freq = get_default("cache_freq")
        gl_date_start = get_default("gl_date_start")
        gl_date_end = get_default("gl_date_end")
        avoid_absolute_paths = get_default("avoid_absolute_paths")

        """ Options """
        r = f"""#Global Options File
# G L O B A L   O P T I O N S   F I L E   -------------------------------------------------------    
cache_freq : {cache_freq}  
gl_date_start : {gl_date_start}   
gl_date_end : {gl_date_end}
avoid_absolute_paths : {avoid_absolute_paths}
{GSEP}"""
        print(r)
        return r

    return create_content()


def content_from_SetupInputsSeries_MainFile(SI: SetupInputsSeries):
    cont = content_from_SetupInputsSeries(SI)
    content = f"{cont}"
    return content


def content_from_SetupInputsOptions_MainFile(SI: SetupInputsConfig):
    cont = content_from_SetupInputsOptions(SI)
    content = f"{cont}"
    return content


# ----------------------------------------------------create_config_series----------------------
def create_config_series(SI: SetupInputsSeries):
    """ Main Aggregated Configuration file for all series """
    config_series_main_file = 'config_series.cfg'
    SetupInputsSeriesRepr = content_from_SetupInputsSeries_MainFile(SI)
    if not is_file(config_series_main_file):
        SetupInputsSeriesRepr = series_title + "\n" + SetupInputsSeriesRepr
    WriteAdd(config_series_main_file, SetupInputsSeriesRepr)

    """ Individual Series ( Each call create only one set of series) """
    create_folder(SI.data_folder)
    series_file_content = content_from_SetupInputsSeries(SI)
    Write(str(Path() / SI.data_folder / 'series.txt'), series_file_content)
    return True


# ----------------------------------------------------create_config_config----------------------
def create_config_config(SI: SetupInputsConfig):
    """ Main Aggregated Configuration file for all USER OPTIONS """
    config_options_main_file = 'options.cfg'
    SetupInputsSeriesRepr = content_from_SetupInputsOptions_MainFile(SI)
    Write(config_options_main_file, SetupInputsSeriesRepr)
    print_with_creating_style("writing")
    print_with_creating_style(SetupInputsSeriesRepr)
    return True


# ----------------------------------------------------             ----------------------

def get_item_for_config_type(obj, config_type):
    return obj[config_type]


# ---------------------------------------------------- InputType ----------------------

@dataclass
class InputType:
    items_from_user: list
    explanations: list
    check_funcs: list
    transform_answers: Union[List[callable], Tuple[callable]]
    applyFunc: Callable  # not from config
    SetupInputs: any  # ...


# ----------------------------------------------------start_setup----------------------


def start_setup(
        config_type: configType = configType.Series,
        onsetup: bool = False,
):
    # assert config_type == configType.Series, "config_type not configType.Series "
    """ S E R I E S """
    Series_obj = InputType(
        items_from_user_series,
        explanations_series,
        check_funcs_series,
        transform_answers_series,
        create_config_series,
        SetupInputsSeries
    )

    """ O P T I O N S """
    Config_obj = InputType(
        items_from_user_config,
        explanations_config,
        check_funcs_options,
        transform_answers_options,
        create_config_config,
        SetupInputsConfig
    )

    instance = {configType.Config: Config_obj, configType.Series: Series_obj}[config_type]
    if not onsetup:
        CIS = create_Input_Items(config_type, instance.items_from_user, instance.explanations, instance.check_funcs,
                                 instance.transform_answers)
        print_with_creating_style(CIS)
    else:

        CIS = tuple("" for _ in items_from_user_config)

    instance.applyFunc(instance.SetupInputs(*CIS))


# ----------------------------------------------------start_setup_series----------------------

def start_setup_series():
    msg = f"""

    This process is going to add new series to your configuration file (config_series.cfg)....

    Program will ask couple of questions to complete your series block on your file.

    Pressing `Enter` will accept for default values for the questions.      
    You may update all information later by opening file with your favorite file editor. 
    --------------------------------------


"""

    print_with_creating_style(msg)
    time.sleep(1)
    start_setup(configType.Series)
    return True


# ----------------------------------------------------start_setup_config----------------------


def start_setup_config(onsetup=False):
    file_name_options = "options.cfg"
    msg = f"""
        This process is going to create user options file  (options.cfg)....
        You may also update all info by opening file with your favorite file editor. 
        --------------------------------------
        Program will ask couple of questions to complete your options on your file.

    """
    if onsetup:
        msg = f"""
        creating `{file_name_options}` 
"""

        if file_exists_show_and_return(file_name_options):
            return
    print_with_creating_style(msg)
    time.sleep(1)
    start_setup(configType.Config, onsetup)
    return True


# -----------------------------------------------------------------------------------------
"""
            default_setup
"""


# -----------------------------------------------------------------------------------------


def get_default_setup_answers(config_type: configType = configType.Config):
    default_answers = {
        configType.Series: default_answers_series,
        configType.Config: default_answers_config
    }[config_type]
    return default_answers


def default_setup(config_type: configType = configType.Config):
    print_with_updating_style("Default setup starting....")

    CIS = get_default_setup_answers(config_type)
    create_config_series(SetupInputsSeries(*CIS))
    return True


__all__ = [
    'default_setup',
    'create_config_series',
    'start_setup_series',
    'default_setup',
    'folder_creatable_by_adding',
    'folder_format_check',
    'folder_creatable',
    'get_default_setup_answers'

]
