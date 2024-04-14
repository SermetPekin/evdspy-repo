#------------------------------------check_remove_back_slash----------------
# back_slash = r"\"" # u"\92"
# back_slash = back_slash.replace('"' , "")
back_slash = "\\"

def check_remove_back_slash(folder_name):
    if str(folder_name).startswith(back_slash):
        folder_name = folder_name[1:]
    return folder_name


reg_relative = '^[a-zA-Z0-9_/\\\\]*$'
reg_absolute_and_relative = '^[a-zA-Z0-9_/\\\\:]*$'

import re


def is_relative(folder):
    result = re.match(reg_relative, folder)
    # if result:
    #     print(f"checked ok {folder}")
    # else:
    #     print(f"not ok {folder}")
    return result
