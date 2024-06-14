import random
from dataclasses import dataclass, field
from pathlib import Path
import pandas as pd
from evdspy.EVDSlocal.utils.utils_general import get_random_hash


@dataclass
class FileItem:
    """Class for general use case"""
    dir_path: str
    file_name: str
    full_name: Path = None
    column_names: tuple = None
    summary: str = None
    sample_data: list = None
    df: pd.DataFrame = None
    df_json: str = ""
    short_name: str = field(init=False)
    encoded_name: str = "aa"
    sa_out_file: str = None
    sa_f_out_file: str = None
    cal_out_file: str = None
    sa_df = None
    sa_f_df = None
    cal_df = None
    created_items: list = field(default_factory=list)

    def __post_init__(self):
        self.full_name = Path() / self.dir_path / self.file_name
        self.created_items.append(self)

    def __repr__(self):
        return f"""
FileItem(
    dir : {self.dir_path} , 
    file_name : {self.file_name}
    full_name : {self.full_name}
    sa_out_file : {self.sa_out_file}
    calendar_out_file : {self.cal_out_file}
)

{self.column_names}

"""


def make_eng(text: str) -> str:
    # return text
    dict_ = {
            'ş': 's',
            'ç': 'c',
            'ı': 'i',
            'ü': 'u',
            'ö': 'o',
            'ğ': 'g',
            'İ': 'I',
            'Ş': 'S',
            'Ğ': 'G',
            'Ç': 'C',
            'Ü': 'U',
            'Ö': 'O',

    }

    return text.translate(text.maketrans(dict_))


def file_items_update(files):
    def update(file_item: FileItem):
        file_item.short_name = make_eng(str(file_item.full_name.stem))
        file_item.encoded_name = file_item.short_name
        return file_item

    return tuple(map(update, files))


def mock_file_items():
    items = []
    random.seed(954)
    exts = ("xlsx", "mat", "m", "xml")
    folders = (".", "A", "B", "C")
    for item in range(10):
        name = get_random_hash(5)
        f = FileItem(random.choice(folders), name + "." + random.choice(exts))
        items.append(f)
    return items
