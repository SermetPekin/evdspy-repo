from dataclasses import dataclass
import typing as t


@dataclass
class CommandLineCommandClass:
    name_list: t.Tuple
    func: t.Callable

