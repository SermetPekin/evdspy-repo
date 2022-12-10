#   ----------------------------------------------------------      ExcelSaveClass
from dataclasses import dataclass
import pandas as pd

from evdspy.EVDSlocal.common.colors import print_with_creating_style, print_with_failure_style, \
    print_excel_created_style
from evdspy.EVDSlocal.utils.utils_general import *
from typing import List
from evdspy.EVDSlocal.common.common_imports import *
@dataclass
class ExcelSaveClass():
    df: pd.DataFrame
    file_name: str
    excel_out_ext: str = "xlsx"
    def out_name_format(self, name):
        return f"{name}.{self.excel_out_ext}"
    def save_with_name(self):
        self.current_file_created = self.out_name_format(self.file_name)
        self.df.to_excel(self.current_file_created)
        return True
    def save_with_diff_name(self):
        h = get_random_hash(5)
        self.current_file_created = self.out_name_format(f"{self.file_name}-{h}")
        self.df.to_excel(self.current_file_created)
        return True
    def try_in_order(self, f_list: List[callable]):
        for index, f in enumerate(f_list):
            result = self.try_this(f)
            if result:
                return index, result
        return -1, False
    def try_this(self, f):
        try:
            f()
            return True
        except Exception as exc:
            print(exc)
            return False
    def save_excel__(self):
        index, result = self.try_in_order(
            [
                self.save_with_name,
                self.save_with_diff_name
            ]
        )
        if index > -1:
            print_excel_created_style(f"\n{indent}{self.current_file_created} was created...")
            return True
        print_with_failure_style(f"File  {self.current_file_created} not created...\n\n\n")
        return False
#   ----------------------------------------------------------    / ExcelSaveClass
