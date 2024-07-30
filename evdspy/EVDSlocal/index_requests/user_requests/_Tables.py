import traceback
from dataclasses import dataclass
from typing import Callable, Any
import pandas as pd

# from ..get_series_indexes import get_series

DF = pd.DataFrame
pos_DF = tuple[DF, ...]


def pass_next_apply(fnc: Callable, *args, **kw):
    result = False
    try:
        result = fnc(*args, **kw)
    except Exception:
        traceback.print_exc()
    return result


@dataclass
class Tables:
    list_: tuple[Any, ...]
    fnc: Callable #= get_series
    cache :bool = True

    def get(self) -> DF:
        data_tuple: tuple[DF, ...] = tuple(map(lambda x: pass_next_apply(self.fnc, x, cache=self.cache), self.list_))
        dt = tuple([x for x in data_tuple if isinstance(x, DF)])
        return self.combine(dt)

    def combine(self, data_tuple: pos_DF) -> DF:
        def fnc(df):
            if 'Tarih' in df.columns:
                df.set_index('Tarih', inplace=True)
            return df

        dfs = [fnc(x) for x in data_tuple]
        combined = pd.concat(list(dfs), axis=1, join='outer')
        return combined

    def __call__(self, *args, **kwargs):
        return self.get()


def get_tables_from_str(string) -> tuple[Any, ...]:
    items = string.splitlines()
    return tuple([x.strip() for x in items if 'bie_' in x])


"""
from ..get_series_indexes import get_series

def tes_tableCombine():
    template = \"""

bie_abreserv
bie_ackap2
bie_akonutsat1
bie_akonutsat2
bie_akonutsat3
bie_akonutsat4
\"""
    tables = get_tables_from_str(template)
    table = Tables(tables , get_series , True )
    df = table()
    assert isinstance(df, DF)
"""
