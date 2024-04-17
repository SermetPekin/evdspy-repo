
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
    """
    MenuItem
    """
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
        sleeptime_default = 1
        obj = {"check": sleeptime_default, "setup": sleeptime_default, "get": sleeptime_default,
               "get_categories_main": sleeptime_default}
        self.sleeptime = obj.get(self.name, sleeptime_default)
    def get_screen_clear_bool(self):
        obj = {"check": False, "get": False, "help_": False, "get_categories_main": False}
        self.clear = obj.get(self.name, True)
@dataclass
class MenuMaker:
    menu_items: field(default_factory=List[MenuItem])
    # menu_items_display : field(default_factory=list)
    message: str = "\n" + " " * 25 + f"Selection ? "
    exit_item: bool = True
    exit_: bool = False
    exit_menu_call_back: Callable = do_nothing
    def __post_init__(self):
        self.add_exit_item()
        Screen().clear()
    def exit(self):
        self.exit_ = True
        self.exit_menu_call_back()
        return
        # self.display()
    def menu_header(self):
        width = 60
        def make_indent(element, num=width):
            indent = " " * (num - len(element))
            return f"{indent}{element}"
        def make_center(element, num=width):
            left = " " * round((num - len(element)) / 2)
            return f"{left}{element}"
        menu_title = make_center("M E N U")
        reminder = "to get the latest version:   pip install -U evdspy"
        reminder = make_indent(reminder)
        version_line = make_indent(config.version)
        logo = make_indent("evdspy @2022")
        line_1 = "-" * width
        print_with_info_style(reminder)
        header = f"""
{line_1}
{version_line}
{line_1}
{logo}
{menu_title}
{line_1}
"""
        return header
    def title(self):
        print("\n" * 2)
        print(self.menu_header())
    def add_exit_item(self):
        if self.exit_item:
            exit_menu_item = MenuItem(self.exit, "EXIT (console)")
            self.menu_items = tuple(list(self.menu_items) + [exit_menu_item])
    def make_table(self, items):
        from rich.console import Console
        from rich.table import Table
        def get_color(item: str):
            font_color = "green"
            if "false" in item.lower():
                font_color = "red"
            return font_color
        table = Table(title="M E N U ")
        table.add_column("Select", justify="right", style="cyan", no_wrap=True)
        table.add_column("Job / Request ", style="green")
        table.add_column("Explanation ", justify="right", style="magenta")
        for index, item in enumerate(items):
            font_color = get_color(item.disp)
            table.add_row(f"{index + 1}", str(item.disp).upper(), "", style=font_color)
        console = Console()
        console.print(table)
    def display(self):
        if self.exit_:
            return
        self.make_table(self.menu_items)
        self.get_choice()
    def display_old(self):
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
            rich_sim(wait_seconds, "completing")
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