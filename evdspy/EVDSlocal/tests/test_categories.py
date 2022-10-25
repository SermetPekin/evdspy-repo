from ..index_requests.categories import get_categories
from ..index_requests.datagroups import get_datagroups


def test_get_categories(capsys):
    with capsys.disabled():
        a = get_categories()
        print(a)


def test_get_datagroups(capsys):
    with capsys.disabled():
        a = get_datagroups()
        print(a)
