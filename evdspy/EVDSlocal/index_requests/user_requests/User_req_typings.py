# typings .......................................................... typings
from typing import Union

import pandas as pd

T_str_int_None = Union[str, int, None]
T_str_tuple_None = Union[str, tuple[str], None]
T_tuple_str_int_None = Union[str, int, tuple[str], tuple[int], None]
T_maybeDf = Union[pd.DataFrame, bool, None]

