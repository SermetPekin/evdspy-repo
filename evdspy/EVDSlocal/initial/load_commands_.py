from ..common.prog import rich_sim
from ..messages.error_messages import *
from ..messages.error_classes import *
from evdspy.EVDSlocal.initial.load_modules import LoadModulesClass
from ..config.config import config
from ..initial_setup.initial_setups import *
from ..console.menu import *
from ..requests_.my_cache import delete_cache_folder
from ..setup_project.user_setup import start_setup_series, start_setup_config
from evdspy.EVDSlocal.utils.utils_general import *

##### LoadModulesClass ##############
deb("load_commands was loaded")
from evdspy.EVDSlocal.initial_setup.setup_folders import check_folders_setup_necessary, check_setup
from ..common.colors import *


def check_setup_runtime():
    return not check_folders_setup_necessary()


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


from evdspy.EVDSlocal.initial_setup.api_key_save import save_api_key_to_file
from typing import Callable


def save_api_key_to_file_main(api_key):
    @dataclass
    class transfer():
        get_input: Callable = get_input
        wait: Callable = wait

    save_api_key_to_file(instance=transfer(), api_key_answer=api_key)


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


def check_api_key_with_low_energy(api_key_from_user):
    # check api key with cache
    # send => basic_for_test > performance.lower_energy
    if not apikey_works(api_key_from_user):
        print_with_failure_style(f"Api key did not work! => {api_key_from_user}")
        return False
    print_with_success_style(f"Api key works => {api_key_from_user}")
    return True


def obvious_checks_of_api_key(api_key: str) -> bool:
    conds: tuple = (isinstance(api_key, str), not len(api_key) < 10,)
    return all(conds)


def save_apikey(api_key: str = None):
    if api_key is None or not isinstance(api_key, str):
        return set_apikey_input()
    set_apikey_input(api_key)


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
    if not obvious_checks_of_api_key(api_key_from_user):
        print_with_failure_style(
                f"The text you entered does not meet criteria to be an valid api key. \n"
                f"{indent}(length of api key cannot be less then 10) {api_key_from_user}")
        return False
    """this function will save redundant requests by catching earlier check results """
    if not check_api_key_with_low_energy(api_key_from_user):
        return False
    """"""
    """ SAVE IT TO FILE """
    save_api_key_to_file_main(api_key_from_user)
    """ SAVE IT FOR RUNTIME """
    ApikeyClass().set_api_key_runtime(value=api_key_from_user)
    show_apikey()
    return True


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


def examples():
    examples_get(get)


def csf():
    return create_series_file()


def setup_series():
    start_setup_series()


def setup_user_options():
    start_setup_config(onsetup=False)


def setup_series_steps():
    return setup_series()


def menu(*args, **kw):
    menu_helper()
    # if CurrentState().menu_will_open:
    #     menu_helper()


def menu_onload():
    if CurrentState().menu_will_open:
        menu_helper()


def show_menu():
    menu_helper()


def menu_helper():
    # TODO config
    global menu_already_displayed
    menu_already_displayed = True
    menu_display()
    # if CurrentState().menu_will_open:
    #     menu_display()


def console():
    return -1


def get_develop_vers_main():
    # print_with_updating_style(str(Path.cwd()))
    parent = Path(__file__).parent
    v = Read(Path(parent / ".." / "version__.py"))  # EVDSlocal/ version.py
    return v


def version():
    v = get_develop_vers_main()
    import site
    s = site.getsitepackages()
    site_pack = ""
    f = ""
    if len(s) > 1:
        site_pack = s[1]
        f = "from"
    print_with_success_style(f"evdspy {v} {f} ")
    print_with_info_style(f"evdspy {v} {f} {site_pack}")
    v = f"evdspy {v} {f} {site_pack}"
    return v


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


def menu_display():
    funcs = [
            ("check setup", check),
            ("setup", easy_setup),
            ("create user options file", setup_user_options),
            ("create series file", create_series_file),
            ("add new series group ", setup_series_steps),
            ("get data", get),
            # ("show summary", show),
            ("help", help_),
            ("show api key", show_apikey),
            ("save api key to file", set_apikey_input),
            ("remove cache folders", remove_cache),
            ("version", version),
    ]
    menu_items = list(map(lambda x: MenuItem(x[1], x[0]), funcs))
    MenuMaker(
            menu_items=menu_items,
            exit_menu_call_back=help_
    ).display()


# ---------------------------------------------------------------MAIN LOAD
""" MAIN LOAD """
from evdspy.EVDSlocal.state.current_state import CurrentState

current_state = CurrentState()


def save(*args):
    return save_apikey(*args)


# ---------------------------------------------------------------/ MAIN LOAD

__all__ = [
        'easy_setup',
        'setup',
        'setup_series',
        "setup_series_steps",
        'help_evds',
        'check',
        'get',
        'h',
        'help_evdspy',
        'help_',
        'examples',
        'create_series_file',
        'csf',
        'show',
        'get_df_test',
        'console',
        'menu',
        'menu_onload',
        'version',
        'save_apikey',
        'save',
        'remove_cache'
]
