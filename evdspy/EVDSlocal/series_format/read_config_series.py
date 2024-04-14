from evdspy.EVDSlocal.series_format.populate_series import *
from evdspy.EVDSlocal.log_classes.log_template import *


def read_series_config():
    req = PopulateSeries("config_series.cfg").split_series_file()
    print(req)
    deb(req)
