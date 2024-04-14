from evdspy.EVDSlocal.common.common_imports import *

from .sample_series_content import sample_series

"""
    This file runs only on startup to create some samples to check setup.
    you may change `series.txt` content according to format provided both on 
    readme file and in the text file.  
"""
from evdspy.EVDSlocal.utils.utils_general import *

from evdspy.EVDSlocal.initial.start_options import *


def create_sample_series_text_file():
    with open(default_series_file_name, "w", encoding=ENCODING) as file_:
        file_.write(sample_series)


def on_start_create():
    from pathlib import Path
    f = Path(default_series_file_name)
    if not f.is_file():
        create_sample_series_text_file()
        print(f"{indent} sample file {default_series_file_name} was created...")


__all__ = [
    'on_start_create'
]
