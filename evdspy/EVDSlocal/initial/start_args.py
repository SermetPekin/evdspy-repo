
from ..common.common_imports import *
from dataclasses import dataclass
from ..log_classes.log_template import get_debugger
Name_or_False = TypeVar('Name_or_False', str, bool)
from typing import Optional
@dataclass
class Args:
    args: field(default_factory=tuple) = field(default_factory=tuple)
    # proxy: Name_or_False = False
    proxy: Optional[str] = False
    file_name: Name_or_False = Name_or_False
    def __post_init__(self):
        self.populate_args()
    def populate_args(self):
        self.proxy = self.extract_prop("--proxy")
        self.file_name = self.extract_prop("--file")
    def extract_prop(self, prop):
        for index, item in enumerate(self.args):
            if prop in item:
                if "=" in item:
                    v = item.split("=")[1]
                else:
                    v = self.args[index + 1]
                return v
        return False
import sys
test_args = Args(sys.argv)
deb("test_args" + ",".join(list(sys.argv)))
# print(debug.log_file_name, debug.log_file_path)
# print(debug)