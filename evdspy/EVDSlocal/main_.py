# ------------------------------------------------------
#
#       main_.py
#                           package: evdspy @2022
# ------------------------------------------------------
import time

from .initial.start_args import *
from evdspy.EVDSlocal.initial_setup.setup_folders import check_folders_setup_necessary
from evdspy.EVDSlocal.initial_setup.initial_setups import SetupInitial
from evdspy.EVDSlocal.common.files import Read

test_api_key_set = False
test_args = test_args

from pathlib import Path


def get_develop_vers_main():
    print(Path.cwd())
    parent = Path(__file__).parent
    v = Read(Path(parent / ".." / "__version__.py")) # EVDSlocal/ version.py
    return v

#-------------------------- version ------------------------------
# print(f"version:{get_develop_vers_main()}")
# time.sleep(2)

deb("....setting up...")

# ---------------------------------SetupInitial----setup ---------


if not check_folders_setup_necessary():
    SetupInitial().setup()
    # SetupInitial().create_series_text_ex()

# ---------------------------------SetupInitial----setup ---------



from .initial.load_commands_ import *

assert callable(check)
assert callable(get)
assert callable(menu)

menu_onload()
EV = help_

# menu()
# help_()
