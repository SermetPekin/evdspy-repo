from ..common.common_imports import *
from ..utils.utils_general import *
from ..initial.start_options import *


@dataclass
class ConfigBase(ABC):
    cancel_request_temp: bool = False
    current_mode_is_test: bool = check_if_this_is_pytest()
    projectName: str = 'evdspy'
    interiorFolder = 'EVDSlocal'
    runtime_file_name_root_path = get_current_dir() / '..'
    runtime_file_name_path = get_current_dir() / '..' / "components" / "options.py"
    user_options_file_name = Path.cwd() / 'IO' / 'options.py'
    user_options_file_name_locked = Path.cwd() / 'IO' / 'options-locked.py'


config = ConfigBase()
