from ..common.common_imports import *
import os

opsys_dict = {
    'nt': 'windows',
    'posix': 'linux/mac',
    'default': 'linux/mac'
}
opsys_name = opsys_dict.get(os.name, opsys_dict.get('default', None))
clear_dict = {
    'windows': 'cls',
    'linux/mac': 'clear',
    'default': 'clear'
}
clear_command_name = clear_dict.get(opsys_name, clear_dict.get('default', None))


class Screen:
    def clear(self):
        os.system(clear_command_name)

