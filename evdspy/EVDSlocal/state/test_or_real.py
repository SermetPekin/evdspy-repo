from ..common.common_imports import *
from pathlib import Path


def check_if_this_is_pytest():
    def check():
        path_ = Path(sys.argv[0])
        return "pytest" in str(path_.stem)

    if len(sys.argv) > 0 and check():
        return True
    else:

        return False
