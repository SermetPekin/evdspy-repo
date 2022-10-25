from .index_classes import GeneralIndexesCategories
from ..manual_requests.prepare import PrepareUrl
from evdspy.EVDSlocal.common.files import Write, Read


def get_categories() -> str:
    return GeneralIndexesCategories().create_url()


def get_categories_data():
    csv = GeneralIndexesCategories().get_csv()
    Write("categories_list.txt", csv)
    return csv
