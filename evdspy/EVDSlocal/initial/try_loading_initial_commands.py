
from ..messages.error_classes import *
from evdspy.EVDSlocal.helper.print_m import *
from evdspy.EVDSlocal.initial_setup.setup_folders import check_folders_setup_necessary
if not check_folders_setup_necessary():
    print("setup checked...")
    try:
        from .load_commands_ import *
        # help_evds()
        # setup_now()
        # help_evds()
    except OptionsFileNotLoadedError:
        print("load_commands_ error trying setup")
        time.sleep(3)
        from ..initial_setup.initial_setups import *
        SetupInitial().setup()
else:
    from .load_commands_ import *
    # help_evds()