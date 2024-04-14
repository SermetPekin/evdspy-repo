from ..index_requests.categories import get_categories
from ..index_requests.datagroups import get_datagroups
from ..tests.core_options_test import verbose


# def test_get_categories(capsys):
#     with capsys.disabled():
#         a = get_categories()
#         if verbose :
#             print(a)
#
#
# def test_get_datagroups(capsys):
#     with capsys.disabled():
#         a = get_datagroups()
#         if verbose :
#             print(a)
def test_get_categories(capsys):
    get_categories()


def test_get_datagroups(capsys):
    get_datagroups()
