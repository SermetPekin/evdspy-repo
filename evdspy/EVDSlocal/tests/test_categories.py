
from ..index_requests.categories import get_categories
from ..index_requests.datagroups import get_datagroups

def test_get_categories(capsys):
    get_categories()
def test_get_datagroups(capsys):
    get_datagroups()