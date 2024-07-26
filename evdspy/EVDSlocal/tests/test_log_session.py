
from evdspy.EVDSlocal.session.session_ import *
from evdspy.EVDSlocal.log_classes.log_template import *
session = get_session()
def test_get_session(capsys):
    s = get_session()

def test_log():
    deb, deb2, debug = get_debugger()