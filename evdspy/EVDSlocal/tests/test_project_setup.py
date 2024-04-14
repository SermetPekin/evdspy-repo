import evdspy
from evdspy.EVDSlocal.series_format.series_creator import *
from evdspy.EVDSlocal.components.evds_seri_files import *
from evdspy.EVDSlocal.setup_project.user_setup import start_setup_series, create_config_series, SetupInputsSeries, \
    start_setup_config, folder_format_check, folder_creatable, folder_creatable_by_adding, default_setup, \
    get_default_setup_answers, configType

from ..tests.core_options_test import *


# from evdspy.EVDSlocal.setup_project.user_setup import  *


def test_start_setup(capsys):

    CIS = get_default_setup_answers(configType.Series)
    with capsys.disabled():
        if verbose:
            print(SetupInputsSeries(*CIS).__class__.__name__)
            # print(type(SetupInputsSeries(*CIS)))
            ...
    assert "SetupInputsSeries" == SetupInputsSeries(*CIS).__class__.__name__, "SetupInputs(*CIS).__class__.__name__"
    assert issubclass(SetupInputsSeries, SetupInputsSeries), "SetupInputs is not  subclass of SetupInputs"


def test_create_config_series(capsys):

    return # this one is ok. Avoided adding new content to real file
    CIS = get_default_setup_answers(configType.Series)
    ret = create_config_series(SetupInputsSeries(*CIS))
    assert ret is True, "test_create_config_series failed"


def test_folder_creatable_by_adding():
    assert folder_creatable_by_adding("=&)%=") is False
    assert folder_creatable_by_adding(r"C:\Users\UserX\PycharmProjects\evdspy\evdspy44\output44") is False


def test_folder_format_check():
    assert folder_format_check("=&)%=") is False
    assert folder_format_check("xxyy") is True
    assert folder_format_check(r"C:\Users\UserX\PycharmProjects\evdspy\evdspy44\output") is False


# def test_start_setup_series():
#     start_setup_series() is True

def test_get_default_setup_answers():
    isinstance(get_default_setup_answers(), list), "get_default_setup_answers"
