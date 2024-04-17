
from .index_classes import GeneralIndexesCategories
from ..components.options_class import load_options
from ..manual_requests.prepare import PrepareUrl
from evdspy.EVDSlocal.common.files import Write, Read
from ..requests_.ev_request import EVRequest
def get_categories() -> str:
    """get_categories"""
    # EVRequest_: EVRequest = EVRequest()
    return GeneralIndexesCategories(EVRequest_=EVRequest(options_=load_options())).create_url()
def get_categories_data() -> str:
    """get_categories_data"""
    csv = GeneralIndexesCategories(EVRequest_=EVRequest(options_=load_options())).get_csv()
    # Write("categories_list.txt", csv)
    return csv
def get_table_header():
    from rich.table import Table
    table = Table(title="Categories / Kategoriler")
    table.add_column("ID/SayÃ„Â±", justify="right", style="cyan", no_wrap=True)
    table.add_column("Title/BaÃ…Å¸lÃ„Â±k (ENG)", style="magenta")
    table.add_column("Title/BaÃ…Å¸lÃ„Â±k (TR)", justify="right", style="green")
    return table
from typing import List
import typing as t
def get_category_name(code: t.Union[int, str] = 1) -> t.Union[str, None]:
    if isinstance(code, str):
        code = int(code)
    csv_buffer: str = get_categories_data()
    lines = csv_buffer.splitlines()
    list_of_categs = {}
    for item in lines[1:]:
        id, cat_eng, cat_tr = split_wisely(item)
        list_of_categs.update({int(id): cat_tr})
    return list_of_categs.get(code, None)
def display_categories() -> t.Union[List[tuple], None]:
    """display_categories"""
    from rich.console import Console
    csv_buffer: str = get_categories_data()
    table = get_table_header()
    lines = csv_buffer.splitlines()
    list_of_categs = []
    if not lines:
        return
    for item in lines[1:]:
        id, cat_eng, cat_tr = split_wisely(item)
        list_of_categs.append((id, cat_eng, cat_tr,))
        table.add_row(id, cat_eng, cat_tr)
    console = Console()
    console.print(table)
    return list_of_categs
def split_wisely(line: str) -> tuple:
    """split_wisely"""
    parts = line.split(",")
    id, cat_eng, cat_tr = "", "", ""
    if len(parts) == 3:
        id, cat_eng, cat_tr = parts
    if len(parts) == 4:
        id, cat_eng, cat_tr, cat_tr2 = parts
        cat_tr = f"{cat_tr}, {cat_tr2}"
    if id:  # '1.0'
        id = id.split(".")[0]
    return id, cat_eng, cat_tr