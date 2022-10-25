#!/usr/bin/python
# -*- coding: utf-8 -*-

from dataclasses import dataclass

"""
Usage : 

    SingletonOptions().set("default_start_date_user", "UserStartDate")
    SingletonOptions().set("default_end_date_user", "UserEndDate")
    SingletonOptions().set("default_cache_user", "UserCache")
    
    
    SingletonOptions().get_valid_value("default_cache")
    SingletonOptions().get_valid_value("default_start_date")
    SingletonOptions().get_valid_value("default_end_date")
    
    
    
"""

if "__main__" == __name__:
    if True:
        default_series_file_name = "config_series.cfg"
        default_data_folder_name = "SeriesData"
        Avoid_Absolute_Paths_ = True
        Default_Prefix_ = "EVPY_"
        # options_folder_name = r"IO"
        DEBUG_LOG_CANCEL = False
        DEGUB_NOTICE = True
        DEBUG_PRINT = False

        default_cache = "daily"  # nocache / hourly
        default_end_date = "01-12-2030"
        default_start_date = "01-01-2019"
        import os
        # USERNAME = os.getenv("USERNAME")  # or hard coded "Username"
else:

    from ..config.config import *
    from ..initial.start_options import *

from typing import Union, List


@dataclass
class Options:
    default_start_date: str
    default_start_date_user: Union[str, None]
    default_end_date: str
    default_end_date_user: Union[str, None]
    default_cache: str
    default_cache_user: Union[str, None]


from pathlib import Path


def load_options():
    options_ = Options(
            default_start_date=default_start_date,
            default_start_date_user=None,
            default_end_date=default_end_date,
            default_end_date_user=None,
            default_cache=default_cache,
            default_cache_user=None
    )
    return options_


class SingletonOptions(object):
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(SingletonOptions, cls).__new__(cls)
            cls.post_init(cls)
        return cls.instance

    def post_init(cls):
        cls.options_ = load_options()
        # read_user_options_on_load()

    def check(cls):
        disp_message = f"""
       default_cache            :  {cls.options_.default_cache}
       default_cache (User)     :  {cls.options_.default_cache_user}
       default start date       :  {cls.options_.default_start_date}
       default start (User)     :  {cls.options_.default_start_date_user}
       default end date         :  {cls.options_.default_end_date}
       default end date (User)  :  {cls.options_.default_end_date_user}
"""
        return disp_message

    def getitem(cls, attr, default_value=None):
        value = getattr(cls.options_, attr, default_value)

        return value

    def set(cls, attr, value):
        setattr(cls.options_, attr, value)

    def __str__(self):
        # print(self.options_.__dict__)

        return str(self.options_.__dict__)

    def display(self):
        return str(self)
        # cls.options_.(attr) = cls.options_.metadata.( attr)

    def get_valid_value(self, attr: str):
        """ """
        user_preferred_value_or_default: str = self.getitem(f"{attr}_user", None)
        if not user_preferred_value_or_default:
            user_preferred_value_or_default = self.getitem(f"{attr}", None)
        return user_preferred_value_or_default


from evdspy.EVDSlocal.common.files import Read, Write

notsetyet = "not set yet OptionsClassfile"

def read_user_options_on_load():
    """below this file it will be called"""
    opts = SingletonOptions()
    file_name = "options.cfg"
    if not Path(file_name).is_file():
        print(Path(file_name))
        cls = SingletonOptions()
        SingletonOptions().set("default_cache_user", cls.options_.default_cache)
        SingletonOptions().set("default_start_date_user", cls.options_.default_start_date)
        SingletonOptions().set("default_end_date_user", cls.options_.default_end_date)

        # raise "file"
        print("user options file was not found. Program will continue with default options...")
        return



    def read_options_file():
        cont = Read(file_name, "could not read ")
        lines = [x for x in cont.splitlines() if not x.strip().startswith("#")]
        lines = [x.split("#")[0] for x in lines]
        return tuple(lines)

    def get_item_from_content(lines: tuple, item: str = None):
        if item is None:
            return None
        for line in lines:
            if item in line and ":" in line:
                return line.split(":")[1].strip()
        return notsetyet

    lines = read_options_file()
    default_cache_user = get_item_from_content(lines, "cache_freq")
    default_start_date_user = get_item_from_content(lines, "gl_date_start")
    default_end_date_user = get_item_from_content(lines, "gl_date_end")
    SingletonOptions().set("default_cache_user", default_cache_user)
    SingletonOptions().set("default_start_date_user", default_start_date_user)
    SingletonOptions().set("default_end_date_user", default_end_date_user)




def notest():
    a1 = SingletonOptions()
    print(a1.display())

    a2 = SingletonOptions()
    a2.options_.default_cache = "smt else "
    print(a1.display())
    print(a2.display())
    a3 = SingletonOptions()
    print(a3.display())
    a3.set("default_start_date", "1212asd54")
    print(a3.display())
    print(a3.get_valid_value("default_start_date"))
    print(a3.get_valid_value("default_cache"))

# notest()


read_user_options_on_load()
