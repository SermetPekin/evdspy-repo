
from ..common.common_imports import *
from dataclasses import dataclass, field
from ..utils.utils_general import *
from ..components.options_class import Options
from ..messages.error_classes import OptionsFileNotLoadedError
from evdspy.EVDSlocal.initial_setup.api_key_save import get_api_key_from_file_improved
from evdspy.EVDSlocal.config.apikey_class import *
from ..components.options_class import load_options
def get_if_attr_exist(pred, f):
    if pred:
        return f(pred)
    return False
@dataclass
class Credentials:
    options_: Options = field(default_factory=load_options)
    apiKey: Optional[any] = False
    proxy = False
    address: str = "https://evds2.tcmb.gov.tr/service/evds/"
    def __post_init__(self):
        self.apikeyobj = field(default_factory=ApikeyClass)  # ApikeyClass()
        self.get_api_keys()
        if hasattr(self.options_, "proxy_file"):
            self.proxy = get_proxy_from_file(self.options_.proxy_file)
    def get_api_keys(self):
        self.apikeyobj = ApikeyClass()
        # from file
        api_from_file = get_api_key_from_file_improved()
        if api_from_file:
            self.apikeyobj.set_api_key_filetype(api_from_file)
    def __repr__(self):
        return f"""
        apikey: obscured(read_successfully)
        proxy : obscured(read_successfully)
        adres:{self.address}
        """
__all__ = [
    'Credentials'
]