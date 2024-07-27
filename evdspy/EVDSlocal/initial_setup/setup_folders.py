from evdspy.EVDSlocal.common.common_imports import *
from evdspy.EVDSlocal.utils.utils_general import *
from evdspy.EVDSlocal.initial.start_options import *
from ..common.colors import *
from evdspy.EVDSlocal.initial.start_options import default_data_folder_name
import time

DefaultDirs = (default_data_folder_name,)

def get_cache_folder():
    pickle_folder = Path.home() / ".cache" / "evdspy"
    return pickle_folder

def create_cache_folder():
    pickle_folder = get_cache_folder()
    create_directory(str(pickle_folder))

def check_folders_setup_necessary():
    dirs = [Path(".") / x for x in DefaultDirs]
    pickle_folder = get_cache_folder()
    dirs.append(pickle_folder)
    return not all([x.is_dir() for x in dirs])

def check_setup():
    return not check_folders_setup_necessary()

def setup_folders():
    if not check_folders_setup_necessary():
        return
    dirs = [Path() / x for x in DefaultDirs]
    pickle_folder = get_cache_folder()
    dirs.append(pickle_folder)
    NEWLINE = "\n"
    def str_(x: Path):
        return str(x.absolute())
    content = NEWLINE.join(tuple(map(str_, dirs)))
    print_with_success_style(f"""
    Folders will bre created
    ..............................
    {content}
""")
    for item in dirs:
        create_directory(str(item))
        print_with_creating_style(f"Creating directory...{item}" )
