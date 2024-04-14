import evdspy
from evdspy.EVDSlocal.main_ import *

def test_check():
    assert callable(check)
    check()

def test_get():
    assert callable(get)
    get()

def test_help_():
    assert callable(help_)
    help_()

def test_menu():
    assert callable(menu)
    menu()

