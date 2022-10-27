from .index_classes import GeneralIndexesCategories
from ..manual_requests.prepare import PrepareUrl
from evdspy.EVDSlocal.common.files import Write, Read


def get_categories() -> str:
    return GeneralIndexesCategories().create_url()


def get_categories_data():
    csv = GeneralIndexesCategories().get_csv()
    Write("categories_list.txt", csv)
    return csv


def split_wisely(line):
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


def display_categories():
    from rich.console import Console
    from rich.table import Table

    csv_buffer: str = get_categories_data()

    table = Table(title="Categories / Kategoriler")
    table.add_column("ID/Sayı", justify="right", style="cyan", no_wrap=True)
    table.add_column("Title/Başlık (ENG)", style="magenta")
    table.add_column("Title/Başlık (TR)", justify="right", style="green")
    lines = csv_buffer.splitlines()
    if not lines:
        return
    for item in lines[1:]:
        id, cat_eng, cat_tr = split_wisely(item)
        table.add_row(id, cat_eng, cat_tr)

    console = Console()
    console.print(table)
