#from evdspy.EVDSlocal.tests.test_evds_classes import *

# from evdspy.EVDSlocal.tests.test_evds_classes import *
# from evdspy.EVDSlocal.tests.test_main_load import *
#
# from evdspy.EVDSlocal.tests.test_project_setup import *
# from evdspy.EVDSlocal.tests.test_log_session import *
# from evdspy.EVDSlocal.tests.test_requests import *
#
# from evdspy.EVDSlocal.tests.test_apikey_checks import *
# from evdspy.EVDSlocal.tests.test_categories import *
# from evdspy.EVDSlocal.tests.test_main_cmd import *

import evdspy
from evdspy.EVDSlocal.main_ import *

def test_menu():
    assert callable(menu)
    menu()


#-------------- not necessary for now
#
# from .tests.test_series_files import *
# from .tests.test_manual_series import *
