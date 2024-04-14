from evdspy.EVDSlocal.series_format.series_creator import *

from ..tests.core_options_test import *


# def test_SeriesFileFormat(capsys):
#     with capsys.disabled():
#         # print(test_SeriesFileFormat2())
#         ...
#     # SeriesFileFormat
#
#     assert isinstance(test_SeriesFileFormat2()[0],
#                       EvdsSeriesRequestWrapper), "SeriesFileFormat did not get EvdsSeriesRequest Item "
#
#     with capsys.disabled():
#         if verbose:
#             create_series_file_from_Wrapper(test_SeriesFileFormat2(), 'test3.txt')
#         ...


from evdspy.EVDSlocal.series_format.read_config_series import *
from evdspy.EVDSlocal.series_format.populate_series import check_pop_read


# def test_read_series_config2(capsys):
#     read_series_config()
#     with capsys.disabled():
#         if verbose:
#             print(check_pop_read())
#
#
# def test_clean_series_line(capsys):
#     with capsys.disabled():
#         print("*************test_clean_series_line TEST*************")
#         print(PopulateSeries().split_series_file())

    # req = PopulateSeries().split_series_file()

    # print(req )
    # def check_pop_read():
    #     ps = PopulateSeries()
    #     req = ps.split_series_file(content=pop_series_test_content)
    #     deb2(req)
    #     return req

#
# def test_create_locked_series_file(capsys):
#     from evdspy.EVDSlocal.initial.load_modules import LoadModulesClass
#     with capsys.disabled():
#         print("*************test_clean_series_line TEST*************")
#         print(LoadModulesClass().create_locked_series_file())
