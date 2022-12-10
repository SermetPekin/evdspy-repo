from evdspy.EVDSlocal.initial_setup.setup_folders import setup_folders
from ..series_format.series_creator import *


@dataclass
class SetupInitial():
    def setup(self):
        setup_folders()
        # create_setup_file()
        # create_series_text_example()

    def create_series_text_ex(self):
        create_series_text_example()

