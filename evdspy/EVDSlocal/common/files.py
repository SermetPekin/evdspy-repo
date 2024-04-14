from .colors import *

filename = 't.txt'
content = 'aaa'
from ..common.common_imports import *
from typing import Union
from pathlib import Path


class WriteContext:
    def __init__(self, fname, content, msg, mode="w"):
        self.mode = mode
        self.fname = fname
        self.content = content
        self.msg = msg

    def __enter__(self):
        self.file_ = open(self.fname, self.mode, encoding='utf-8')
        self.file_.write(self.content)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.file_.close()
        if exc_tb:
            print_with_failure_style(exc_tb)
            print_with_failure_style(self.msg)
        return True


def Write(fname="test.txt", content="test", msg="Error"):
    info = f"{fname}"

    result = False, "File was not created"
    with WriteContext(fname, content, msg):
        result = True, f"File was created... : {info}"
    return result, f"File was created.. : {info}"


def WriteAdd(fname="test.txt", content="test", msg="Error"):
    info = f"{fname}"
    content = "\n" + content

    result = False, "File was not created"
    with WriteContext(fname, content, msg, mode="a"):
        result = True, f"File was created... : {info}"
    return result, f"File was created.. : {info}"


class ReadContext:
    def __init__(self, fname, msg):
        self.fname = fname
        self.msg = msg

    def __enter__(self):
        # self.file_ = open(self.fname, "r", encoding='utf-8')
        self.file_ = open(self.fname, "r", encoding='utf_8_sig')
        return self.file_

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.file_.close()
        if exc_tb:
            print_with_failure_style(exc_tb)
            print_with_failure_style(self.msg)
            return False
        return True


def Read(file_name: Union[str, Path], msg="Error"):
    if isinstance(file_name, str):
        file_name = Path(file_name)
    content = ""
    with ReadContext(file_name, msg) as file_:
        content = file_.read()
    return content


def create_folder(folder_name: Union[str, Path]):
    if isinstance(folder_name, str):
        folder_name = Path(folder_name)
    try:
        os.makedirs(folder_name)
    except FileExistsError:
        print_with_updating_style("folder {} already exists".format(folder_name))
    except Exception as e:
        print_with_failure_style(e)


def is_file(path_: str):
    d = Path(path_)
    return d.is_file()


def is_dir(path_: str):
    d = Path(path_)
    return d.is_dir()


def WriteBytes(file_name: str, content_bytes: bytes):
    with open(file_name, 'wb') as f:
        f.write(content_bytes)


def WriteBytesAdd(file_name: str, content_bytes: bytes):
    with open(file_name, 'ab') as f:
        f.write(content_bytes)


def ReadBytes(file_name: str):
    with open(file_name, "rb") as f:
        return f.read()


def make_indented(content: str, indent=" " * 10) -> str:
    content_tup: tuple = tuple(f"{indent}{x}" for x in content.splitlines())
    content = "\n".join(content_tup)
    return content


def add_one_line(cont_tuple: tuple, line: str) -> tuple:
    cont: list = list(cont_tuple)
    new_cont = cont + [line]
    return tuple(new_cont)


# def content_continues_line(content: str) -> str:
#     content = make_indented(content)
#     content = make_it_summary(content, add_continue=True)
#     return content
def line_continues_fn(skipped=0):
    def cont_fn():
        lns = "lines"
        if skipped == 1:
            lns = "line"
        if skipped > 0:
            msg = f"{skipped} {lns} more..."
            # skipped_msg = "" if skipped > 0 else f"{skipped} line more..."
            cont = "." * 15 + f"{msg}" + "." * 15
            print_with_style(f"{cont}\n")
        ...

    return cont_fn


def make_it_summary(content: str, max_line_num: int = 10, add_continue: bool = False) -> tuple:
    content_tup: tuple = tuple(f"{x}" for x in content.splitlines())
    new_content_tup: tuple = content_tup[0:max_line_num]
    skipped_lines = len(content_tup) - max_line_num if len(content_tup) - max_line_num > 0 else 0
    new_content_tup = add_one_line(new_content_tup, "." * 15)
    return "\n".join(new_content_tup), skipped_lines


def file_exists_show_and_return(file_name: Union[str, Path]) -> bool:
    if isinstance(file_name, str):
        file_name = Path(file_name)
    if file_name.is_file():
        content_ = Read(file_name)
        print_with_updating_style(f"file {file_name} exists, not replacing...\n")
        print_with_color("content: \n -------\n", "blue")
        cont_msg, skipped = make_it_summary(make_indented(content_), add_continue=False, max_line_num=10)
        print(cont_msg)
        """print fn will return """
        line_continues_fn(skipped)()
        time.sleep(1)
        return True
    return False
