import sys
from pathlib import Path


class NOArgsEror(BaseException):
    """NOArgsEror"""


def arg_acc(argv=tuple(sys.argv)):
    if argv is None:
        raise NOArgsEror
    obj = {}
    for index, key in enumerate(argv):
        key = str(key)
        if key.startswith("--"):
            value = None
            if len(argv) > index + 1:
                value = argv[index + 1]
            key = key[2:]
            obj.update({key: value})
    return obj


# --------------------------------------------------------------------------------------
# T E S T   E N V I R O N M E N T
# --------------------------------------------------------------------------------------
rf"""
 Usage 
    echo on 
    cd C:\Users\Username\PycharmProjects\evdspy
    python setup.py bdist_wheel --universal --folder C:\Username\SomeFolder\Env
    @params 
        --folder : Test Env folder \
        --stable : status (dev : False / prod : True )
"""


def check_stable(STABLE_FORCE_, get_args_dict_runtime):
    """Stable Version or Development with time and date"""
    args_dict = get_args_dict_runtime()
    stable_param = args_dict.get("stable", None)
    stable = True if stable_param == "True" or STABLE_FORCE_ else False
    return stable


def create_env_folder(test_environment_):
    path = Path(test_environment_)
    if not path.is_dir():
        import os
        os.makedirs(path)


def get_cmd_file(get_args_dict_runtime):
    cmd_file = False
    test_env = get_test_env(get_args_dict_runtime)
    if test_env:
        cmd_file = 'Run_produced'
        create_env_folder(test_env)
        """ nick name for the env for simplicity"""
        if isinstance(test_env, str):
            nick_name_for_env = Path(test_env).parts[-1]
            """ command file to install development/pord version in local area"""
            cmd_file = f"{cmd_file}-{nick_name_for_env}.cmd"
    return cmd_file


def get_test_env(get_args_dict_runtime):
    args_dict = get_args_dict_runtime()
    test_environment__ = False
    """ Test Env folder """
    folder = args_dict.get("folder", None)
    if folder is None:
        folder = args_dict.get("--folder", None)
    if folder:
        test_environment__ = folder
        # normalize parameters for standard build
        sys.argv = sys.argv[0: 3]
    return test_environment__


def get_args_dict(args):
    args_dict = arg_acc(args)
    return args_dict
