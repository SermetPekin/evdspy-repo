# from ..before_main_ import *

from evdspy.EVDSlocal.initial_setup.setup_folders import setup_folders

# from ..setup_options import *
# from ..setup_options import copy_setup_file
from ..series_format.series_creator import *


@dataclass
class SetupInitial():
    def setup(self):
        setup_folders()
        # create_setup_file()
        # create_series_text_example()

    def create_series_text_ex(self):
        create_series_text_example()

    # def only_copy(self):
    #     copy_setup_file()