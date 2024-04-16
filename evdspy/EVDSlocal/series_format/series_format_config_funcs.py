
from ..common.common_imports import *
TrueFunc = (lambda x: True)
def folder_creatable(folder):
    try:
        d = Path(folder)
        if d.is_dir():
            return True
    except:
        return False
    return False
def folder_creatable_by_adding(folder):
    try:
        d = Path(folder)
        e = str(d).replace(d.stem, "")
        if not len(e) > 0:
            return False
        f = Path(e)
    except:
        return False
    return folder_creatable(f)
from evdspy.EVDSlocal.common.folder_name_checks import is_relative
from rich import print
from rich.console import Console
from rich.theme import Theme
custom_theme = Theme({
    "info": "dim cyan",
    "warning": "magenta",
    "danger": "bold red"
})
console = Console(theme=custom_theme)
# console.print("test info", style="info")
# console.print("[warning]test warning[/warning]")
# console.print("Test", style="danger")
def folder_format_check(folder: str):
    if not folder.strip():
        return True
        # print(f"checking ... {folder}")
    console.print(f"checked foldername :  {folder}", style="warning")
    import string
    if isinstance(folder, str) and is_relative(folder):
        return True
    print("[danger]folder name does not fit to format[/danger]")
    return False
def notest():
    t = is_relative(r"/asfasdf/asdfasdf")
    is_relative(r"C:/asfasdf/asdfasdf??")
    is_relative(r"C:/asfasdf/asdfasdf??")
    is_relative(r"asfasdf/asdfasdf")
notest()