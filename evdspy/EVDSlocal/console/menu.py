from ..common.common_imports import *
from collections import namedtuple
from dataclasses import dataclass, field
from ..config.config import *
from evdspy.EVDSlocal.console.screen import *
from ..common.prog import rich_sim
from ..common.colors import *

# from evdspy.utils.utils_general import *

indent = " " * 15

# MenuItem = namedtuple("MenuItem", "func disp sleeptime clear")
# MenuItem = namedtuple("MenuItem", "func disp sleeptime clear")
from typing import Union, List, Tuple, Callable

do_nothing = lambda: True


@dataclass
class MenuItem:
    func: Union[Callable, str]
    disp: str
    sleeptime: int = 0
    clear: bool = False
    name: str = ""
    callable_func: Callable = do_nothing

    def __post_init__(self):
        if callable(self.func):
            self.name = self.func.__name__
            self.callable_func = self.func
        elif isinstance(self.func, str):
            self.name = self.func
        else:
            self.name = self.disp

        self.get_sleep_times()
        self.get_screen_clear_bool()

    def get_sleep_times(self):
        obj = {"check": 1, "setup": 2, "get": 2}
        self.sleeptime = obj.get(self.name, 1)

    def get_screen_clear_bool(self):
        obj = {"check": False, "get": False, "help_": False}
        self.clear = obj.get(self.name, True)


@dataclass
class MenuMaker:
    menu_items: field(default_factory=List[MenuItem])
    # menu_items_display : field(default_factory=list)
    message: str = "\n" + " " * 25 + f"Selection ? "
    exit_item: bool = True
    exit_ = False
    exit_menu_call_back: Callable = do_nothing

    def __post_init__(self):
        self.add_exit_item()
        Screen().clear()

    def exit(self):
        self.exit_ = True
        self.exit_menu_call_back()
        return
        # self.display()

    def title(self):

        print("\n" * 2)
        print_with_info_style("-" * 50)
        print_with_info_style(" " * 20 + " M E N U " + " " * 21)
        print_with_info_style("-" * 50)

    def add_exit_item(self):
        if self.exit_item:
            exit_menu_item = MenuItem(self.exit, "console")
            self.menu_items = tuple(list(self.menu_items) + [exit_menu_item])

    def display(self):

        if self.exit_:
            return
        self.title()
        for index, item in enumerate(self.menu_items):
            dec = f"{indent}{index + 1}. {item.disp} "
            print_menu_item_style(dec)
        self.get_choice()

    def menu_exists_and_callable(self, a: str):
        if str(a).isnumeric() and int(a) in (x for x in range(1, len(self.menu_items) + 1)):
            menu_item: MenuItem = self.menu_items[int(a) - 1]
            func = menu_item.func
            return callable(func), menu_item.callable_func, menu_item
        return False, False, False

    def get_choice(self):
        if self.exit_:
            return
        if config.current_mode_is_test:
            return
        ans = input(self.message)
        cond, func, menu_item = self.menu_exists_and_callable(ans)

        if cond:
            wait_seconds = menu_item.sleeptime

            if menu_item.clear:
                Screen().clear()
            v = func()
            if v == -1:
                self.exit_ = True
            # print("done...returning to menu...")
            rich_sim(wait_seconds, "completing")
            # time.sleep(wait_seconds)
        else:
            Screen().clear()
        return self.display()


__all__ = [
        'MenuItem',
        'MenuMaker',
]


def test_show():
    print("test")


def test_show2():
    print("test 2")


def test_show3():
    print("test 3")


def test_f():
    t1 = MenuItem(test_show, "test_show")
    t2 = MenuItem(test_show2, "test_show2")
    t3 = MenuItem(test_show3, "test_show3")
    m = MenuMaker(menu_items=[t1, t2, t3])
    m.display()

