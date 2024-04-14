from evdspy.EVDSlocal.setup_project.user_setup_helper import *

from evdspy.EVDSlocal.components.populate_series import *
from evdspy.EVDSlocal.logs.log_template import *


def read_series_config():
    req = PopulateSeries("config_series.cfg").split_series_file()
    print(req)
    deb(req)
