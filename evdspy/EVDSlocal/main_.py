
# ------------------------------------------------------
#
#       main_.py
#                           package: evdspy @2022
# ------------------------------------------------------
from .initial.start_args import *
import typing as t
def print_with_failure_style(msg):
    print(msg)
def print_with_success_style(msg):
    print(msg)
def check_compat():
    import platform
    v_tuple = platform.python_version_tuple()
    # v_tuple = "3.6.0".split(".")
    v_tuple = tuple(map(lambda x: int(x), v_tuple))
    v = sys.version  # sys.version_info
    if (4, 1, -1) < v_tuple:
        print_with_failure_style(
            f"Your python version is {v}. This program may break because it is currently only compatible with versions between 3.7 and 3.11")
        return False
    elif (3, 7, 0) > v_tuple:
        print_with_failure_style(
            f"Your python version is {v}. This program may break because it is currently only compatible with versions between 3.7 and 3.11")
        return False
    else:
        # print_with_success_style(
        #     f"Your python version is {v} This program was tested with this version and runs properly. However, "
        #     f"if you notice a bug or if your version breaks at runtime please feel free to open a PR on github.")
        return True
if not check_compat():
    import sys
    sys.exit(0)
def register_actions(actions=None) -> tuple:
    if actions is None:
        actions = []
    """register_actions"""
    from evdspy.EVDSlocal.initial_setup.initial_setups import SetupInitial
    actions.append(SetupInitial().setup)
    # actions.append( SetupInitial().create_series_text_ex   )
    return tuple(actions)
def do_start(actions: t.Tuple[t.Callable]):
    """CHECK => SETUP , START ==> or => START"""
    from evdspy.EVDSlocal.initial_setup.setup_folders import check_folders_setup_necessary
    if not check_folders_setup_necessary():
        for action in actions:
            if callable(action):
                deb(f"....setting up....starting..{action.__name__}")
                action()
def initial_checks_after_first_run():
    """initial_checks_after_first_run"""
    assert callable(check)
    assert callable(get)
    assert callable(menu)
# --------------------------------- M A I N ---------
do_start(register_actions())
from evdspy.EVDSlocal.initial.load_commands_ import *
initial_checks_after_first_run()
# --------------------------------- / M A I N ---------