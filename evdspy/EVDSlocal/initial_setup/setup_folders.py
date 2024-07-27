
from evdspy.EVDSlocal.common.common_imports import *
from evdspy.EVDSlocal.utils.utils_general import *
from evdspy.EVDSlocal.initial.start_options import *
from ..common.colors import *
from evdspy.EVDSlocal.initial.start_options import default_data_folder_name
# dirs = ("pickles", default_data_folder_name)
dirs = ( default_data_folder_name , )
cur_folder = Path()
import time

def get_cache_folder():
    pickle_folder = Path.home() / ".cache" / "evdspy"
    return pickle_folder
def create_cache_folder():
    pickle_folder =get_cache_folder()
    create_directory(str(pickle_folder))
def check_folders_setup_necessary():
    for item in dirs:
        folder_ = cur_folder.absolute() / item
        if not folder_.is_dir():
            return True
    pickle_folder =get_cache_folder()
    
    return pickle_folder.is_dir()
def check_setup():
    return not check_folders_setup_necessary()
def setup_folders():
    
    if not check_folders_setup_necessary():
        return
    create_cache_folder()
    for item in dirs:
        folder_ = cur_folder.absolute() / item
        print_with_creating_style(f"Creating directory...{folder_}")
        create_directory(str(folder_))
        time.sleep(0.8)
