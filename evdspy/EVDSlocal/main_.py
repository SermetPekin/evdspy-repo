# ------------------------------------------------------
#
#       main_.py
#                           package: evdspy @2022
# ------------------------------------------------------
from .initial.start_args import *
import typing as t


def register_actions(actions=None)->tuple  :
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
from .initial.load_commands_ import *
initial_checks_after_first_run()
# --------------------------------- / M A I N ---------
