
# functions that will be loaded
import platform
import sys
import time
import pandas as pd
from evdspy.EVDSlocal.console.menu import MenuMaker, MenuItem
from .cmd_line_classes import CommandLineCommandClass
from evdspy.EVDSlocal.initial_setup.api_key_save import save_api_key_to_file
from typing import Callable
from ..common.prog import rich_sim
from ..common.table import Table2_
from ..index_requests.categories import get_category_name
from ..index_requests.datagroup_individual import get_datagroup_individual_with_code, get_series_list_of_subject, \
    get_df_datagroup
from ..messages.error_messages import *
from ..messages.error_classes import *
from evdspy.EVDSlocal.initial.load_modules import LoadModulesClass
from ..initial_setup.initial_setups import *
from ..requests_.my_cache import delete_cache_folder
from ..setup_project.user_setup import start_setup_series, start_setup_config
from evdspy.EVDSlocal.initial_setup.setup_folders import check_folders_setup_necessary, check_setup
from ..messages.help_messages import welcome_message
from ..utils.utils_general import *
from ..index_requests.datagroups import get_datagroups_with_code
assert get_datagroups_with_code
assert get_category_name
assert get_series_list_of_subject
"""
Loaded functions for DF
get_df_datagroup
"""
assert callable(get_df_datagroup)
def check_which_command_params(params, extra_params: dict):
    create_series_cmd = CommandLineCommandClass(name_list=("create", "series",),
                                                func=setup_series)
    help_cmd = CommandLineCommandClass(name_list=("help",),
                                       func=help_evds)
    create_options_cmd = CommandLineCommandClass(name_list=("create", "options",),
                                                 func=create_options_file)
    get_cmd = CommandLineCommandClass(name_list=("get",), func=get)
    setup_cmd = CommandLineCommandClass(name_list=("setup",), func=setup)
    menu_cmd = CommandLineCommandClass(name_list=("menu",), func=menu)
    save_cmd = CommandLineCommandClass(name_list=("save",), func=save)
    console_cmd = CommandLineCommandClass(name_list=("console",), func=console_load)
    menu_list = (create_series_cmd, create_options_cmd, get_cmd, setup_cmd, menu_cmd, help_cmd, save_cmd, console_cmd)
    def check_item_exists(element, format_cmd_list):
        return element in format_cmd_list
    def check_item_exists_wrapper(item):
        return check_item_exists(item, params)
    def check_cmd_will_apply(cmd_class: CommandLineCommandClass):
        # return check_item_exists, items
        return all(map(check_item_exists_wrapper, cmd_class.name_list))
    from itertools import compress
    functions_will_apply_iter = tuple(map(check_cmd_will_apply, menu_list))
    functions_will_apply = list(compress(menu_list, functions_will_apply_iter))
    for fnc_class in functions_will_apply:
        if callable(fnc_class.func):
            fnc_class.func()
    return functions_will_apply
def menu():
    """
    Displays user-friendly menu screen for many functionalities
    such as saving API key, getting data, categories etc.
    :return: None
    """
    menu_helper()
# -------------------------------- Entry point ---cmd line prompt------------------------------------
def console_main(test_args=None):
    # test_args = tuple(["series", "create"])
    if test_args:
        params_command = test_args
    else:
        params_command = sys.argv[1:]
    params_command_as_dict = arg_acc(params_command)
    if not params_command:
        welcome_message()
    check_which_command_params(params_command, arg_acc())
# -------------------------------- Entry point ---cmd line prompt------------------------------------
def console_main_from_the_menu():
    welcome_message()
def easy_setup():
    setup()
def setup_again():
    setup()
def setup():
    SetupInitial().setup()
    start_setup_config(onsetup=True)
    create_series_text_example(onsetup=True)
def help_evds():
    display_help_messages()
def help_():
    return help_evds()
def h():
    return help_evds()
def help_evdspy():
    return help_evds()
def check():
    print_with_updating_style("checking....")
    lmc = LoadModulesClass()
    lmc.check()
def show():
    lmc = LoadModulesClass()
    lmc.series_from_file()
    lmc.summary()
def get_input(msg):
    if config.current_mode_is_test:
        return "test"
    print_get_input_style(msg)
    ans = input()
    return str(ans)
def wait(num: int):
    time.sleep(num)
def save_api_key_to_file_main(api_key):
    @dataclass
    class transfer():
        get_input: Callable = get_input
        wait: Callable = wait
    save_api_key_to_file(instance=transfer(), api_key_answer=api_key)
def console_load():
    ...
def check_setup_runtime():
    return not check_folders_setup_necessary()
def check_if_api_set_before_get():
    if not check_api_key():
        print_with_failure_style(api_key_not_set_msg)
        wait(2)
        if not get_input("yes/no ?  ").lower() in ["yes", "y"]:
            wait(2)
            return
        # below the function checks
        # if api key is valid then saves it
        if not set_apikey_input():
            return False
        print_with_success_style("finished")
        return True
    return True
def get():
    if not check_setup():
        print_with_updating_style("Checking setup...")
        # setup_folders()
        SetupInitial().setup()
    if not check_if_api_set_before_get():
        return
    try:
        lmc = LoadModulesClass()
        lmc.series_from_file()
        # lmc.display_items(lmc.series_from_file())
        lmc.summary()
        # try:
        #     lmc.evds_list[0].df.plot(x='TP.ODEMGZS.BDTTOPLAM', y='Index', style='o')
        # except:
        #     pass
    except SeriesFileDoesNotExists:
        print("...")
        # print(SeriesFileDoesNotExists().message)
def get_df_test():
    LoadModulesClass().series_from_file()
    LoadModulesClass().summary()
    return LoadModulesClass().evds_list[0].df
from ..config.apikey_class import *
from evdspy.EVDSlocal.requests_.lower_energy import *
from rich import inspect
from typing import List
from evdspy.EVDSlocal.index_requests.datagroups import get_and_process_datagroups_with_code, \
    get_all_groups, get_datagroups_with_code
from evdspy.EVDSlocal.index_requests.index_util_funcs import json_to_df
import typing as t
from functools import partial
def get_input_for_categs_data_groups(list_of_categs: List[tuple], display_fn, callback: t.Callable = None):
    callback_forward = partial(get_input_for_categs_data_groups, list_of_categs, display_fn, None)
    callables = (display_fn, callback_forward)
    if config.current_mode_is_test:
        return
    ids = (str(x[0]) for x in list_of_categs)
    # print_with_success_style('Preparing the menu...')
    # print("\n\n")
    # time.sleep(2)
    ans = input("Choose a Category number [e/exit to go back] Selection Number==>")
    if str(ans).lower().strip() in ('e', 'exit'):
        if callable(callback):
            print("now calling back ", display_fn, callback)
            display_fn()
            callback()
        return
    if str(ans) in ids:
        codes_and_titles = get_and_process_datagroups_with_code(int(ans))
        get_input_for_categs_data_groups_deeper(codes_and_titles, callables)
def get_input_for_categs_data_groups_deeper(codes_and_titles: List[tuple], callables: t.Tuple[any, partial] = None):
    codes = tuple(x[0] for x in codes_and_titles)
    nums = tuple(str(x + 1) for x in range(len(codes_and_titles)))
    titles = tuple(x[1] for x in codes_and_titles)
    combine_list = list(zip(nums, codes, titles))
    if config.current_mode_is_test:
        return
    # print(codes_and_titles)
    # print("\n\n")
    Table2_().show(list_=combine_list, title='', columns=('Selection Number', 'code', 'title'), skiprow=0)
    # print_with_success_style('Preparing the menu...')
    # time.sleep(2)
    ans = input("Choose a Category number  [e/exit to go back]  Selection Number==>")
    if str(ans).lower().strip() in ('e', 'exit'):
        if callables:
            for callback in callables:
                if callable(callback) or isinstance(callback, partial):
                    callback()
                    time.sleep(1)
        return
    if str(ans) in nums:
        code_str = codes[int(ans) - 1]
        try:
            json_content = get_datagroup_individual_with_code(code_str)
            # print(json_content)
            df = json_to_df(json_content)
            print(df.head())
            series_docs = get_series_list_of_subject(code_str)
            df_exp: pd.DataFrame = json_to_df(series_docs)
            print_with_success_style(
                    "Getting explanations for the series...after this process both excel files will be created...[1-Data , 2-Explanations] "
            )
            time.sleep(1)
            print(df_exp.head())
            # print(series_docs)
        except:
            print_with_failure_style(
                    f"...json  content is not proper to convert to a pd.DataFrame .. passing this one... code : {code_str}")
            pass
        df_exp: pd.DataFrame = json_to_df(series_docs)
        print_with_success_style(
                "Getting explanations for the series...after this process both excel files will be created...[1-Data , 2-Explanations] "
        )
        time.sleep(1)
        print(df_exp.head())
        # print(series_docs)
    print(ans, " ... done.")
    get_input_for_categs_data_groups_deeper(codes_and_titles, callables)
    # codes_and_titles = get_and_process_datagroups_with_code(int(ans))
    # get_input_for_categs_data_groups_deeper(codes_and_titles)
def get_categories_main():
    if not check_if_api_set_before_get():
        return
    # from ..index_requests.categories import get_categories_data
    from ..index_requests.categories import display_categories
    list_of_categs: List[tuple] = display_categories()  # [( id , eng , tr ) , ( id , eng , tr ) ...]
    get_input_for_categs_data_groups(list_of_categs, display_fn=display_categories)
    # categories = get_categories_data()
    # inspect(categories, all=True)
    # print_with_success_style(categories)
def get_datagroups_data_main():
    ...
    # from ..index_requests.datagroups import get_datagroups_data
    # categories = get_datagroups_data()
    # inspect(categories, all=True)
    # print_with_success_style(categories)
def check_api_key_with_low_energy(api_key_from_user):
    # check api key with cache
    # send => basic_for_test > performance.lower_energy
    if not apikey_works(api_key_from_user):
        print_with_failure_style(f"Api key did not work! ")
        return False
    print_with_success_style(f"Api key works")
    return True
def obvious_checks_of_api_key(api_key: str) -> bool:
    conds: tuple = (isinstance(api_key, str), not len(api_key) < 10,)
    return all(conds)
def save_apikey(api_key: str = None):
    if api_key is None or not isinstance(api_key, str):
        return set_apikey_input()
    check_apikey_and_then_save(api_key)
def check_apikey_and_then_save(api_key_from_user):
    if not obvious_checks_of_api_key(api_key_from_user):
        print_with_failure_style(
                f"The text you entered does not meet criteria to be an valid api key. \n"
                f"{indent}(length of api key cannot be less then 10)  ")
        return False
    """this function will save redundant requests by catching earlier check results """
    if not check_api_key_with_low_energy(api_key_from_user):
        return False
    """"""
    """ SAVE IT TO FILE """
    save_api_key_to_file_main(api_key_from_user)
    """ SAVE IT FOR RUNTIME """
    ApikeyClass().set_api_key_runtime(value=api_key_from_user)
    # show_apikey()
    return True
def set_apikey_input(api_key=None, from_console=False):
    exit_words = ["e", "exit"]
    if config.current_mode_is_test:
        print_with_updating_style("pytest returns ")
        ans = "test"
    else:
        if not from_console:
            ans = get_input("Api key [ `e` or `exit` to cancel] : ")
        else:
            ans = api_key
    api_key_from_user = str(ans)
    if api_key_from_user.lower() in exit_words:
        print_with_updating_style("exited")
        return False
    return check_apikey_and_then_save(api_key_from_user)
from evdspy.EVDSlocal.initial_setup.api_key_save import check_api_key_on_load
def check_api_key():
    check_api_key_on_load()
    apikeyobj = ApikeyClass()
    return apikeyobj.get_valid_api_key()
def show_apikey():
    apikeyobj = ApikeyClass()
    # k = apikeyobj.get_api_keys_dict()
    valid = apikeyobj.get_valid_api_key()
    disp = f"""
    valid api key : {valid}
"""
    print_with_success_style(disp)
from ..series_format.series_creator import *
def create_series_file():
    return create_series_text_example()
def csf():
    return create_series_file()
def setup_series():
    start_setup_series()
def setup_user_options():
    start_setup_config(onsetup=False)
def create_options_file():
    setup_user_options()
def cof():
    create_options_file()
def setup_series_steps():
    return setup_series()
def console():
    return -1
def get_develop_vers_main():
    # print_with_updating_style(str(Path.cwd()))
    parent = Path(__file__).parent
    v = Read(Path(parent / ".." / ".." / "__version__.py"))  # EVDSlocal/ version.py
    return v
def version():
    from evdspy.EVDSlocal.console.menu_logo_header import version_logo
    logo_version, reminder = version_logo()
    print_with_success_style(logo_version)
    print_with_info_style(reminder)
def py_version():
    from platform import python_version
    #
    # print_with_creating_style(sys.version_info)
    # print_with_creating_style(python_version())
    print_with_creating_style(sys.version)
    # print_with_creating_style(str(platform.python_version_tuple()))
def check_compat():
    v_tuple = platform.python_version_tuple()
    # v_tuple = "3.6.0".split(".")
    v_tuple = tuple(map(lambda x: int(x), v_tuple))
    v = sys.version  # sys.version_info
    if (3, 11, -1) < v_tuple:
        print_with_failure_style(
                f"Your python version is {v}. This program may break because it is currently only compatible with versions between 3.7 and 3.11")
    elif (3, 7, 0) > v_tuple:
        print_with_failure_style(
                f"Your python version is {v}. This program may break because it is currently only compatible with versions between 3.7 and 3.11")
    else:
        print_with_success_style(
                f"Your python version is {v} This program was tested with this version and runs properly. However, "
                f"if you notice a bug or if your version breaks at runtime please feel free to open a PR on github.")
def save(*args):
    return save_apikey(*args)
def remove_cache():
    # TODO activate
    msg = "This will attempt to delete cache files in order to make new requests. \n " \
          "If you created your options file you may choose caching period to a more frequent one. \n" \
          "this function was added to force making new requests ignoring recent ones. \n" \
          "Proceed? (Y/n)"
    ans = get_input(msg)
    if not ans in ["y", "Y"]:
        print_with_failure_style("exited without removing the cache")
        return
    print_with_success_style("removing cache...")
    if delete_cache_folder():
        rich_sim(3, "processing...")
        print_with_success_style("cahce folder removed...")
    else:
        print_with_failure_style("cahce folder coould not be removed...")
def testt_the_latest():
    get_all_groups()
    # get_and_process_datagroups_with_code(3)
    # def __():
    #     *coming, last = get_datagroups_df('json', None, True)
    #     print(coming)
    #     print(last)
    #     print(last())
def main_exit_function():
    ...
def menu_display():
    funcs = [
            ("check setup", check),
            ("setup", setup),
            ("create user options file", create_options_file),
            ("create series file", create_series_file),
            ("add new series group ", setup_series_steps),
            ("get data", get),
            ("get categories (get all series of a datagroup)", get_categories_main),  # next version
            # ("get data groups (on development) ", get_datagroups_data_main),  # next version
            ("help", help_),
            ("show api key", show_apikey),
            ("save api key to file", set_apikey_input),
            ("remove cache folders", remove_cache),
            ("evdspy as a command line prompt", console_main_from_the_menu),
            ("version", version),
            ("py version", py_version),
            ("check compatibility of your python version", check_compat),
    ]
    if 'NEXT_RELEASE' in str(Path().cwd()):
        funcs.append(('test_the latest', testt_the_latest))
    menu_items = list(map(lambda x: MenuItem(x[1], x[0]), funcs))
    MenuMaker(
            menu_items=menu_items,
            exit_item=True,
            exit_menu_call_back=main_exit_function
    ).display()
def menu_helper():
    # TODO config
    global menu_already_displayed
    menu_already_displayed = True
    menu_display()
def menu_onload():
    if CurrentState().menu_will_open:
        menu_helper()
def show_menu():
    menu_helper()
# get_df_datagroup = get_df_datagroup