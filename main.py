import pandas as pd

from evdspy import get_series, get_series_exp

template = """TP_GSYIH01_GY_CF
TP_GSYIH02_GY_CF
TP_GSYIH03_GY_CF
TP_GSYIH04_GY_CF
TP_GSYIH05_GY_CF
TP_GSYIH06_GY_CF
TP_GSYIH07_GY_CF
TP_GSYIH08_GY_CF
TP_GSYIH09_GY_CF
TP_GSYIH10_GY_CF
TP_GSYIH11_GY_CF
TP_GSYIH14_GY_CF
TP_GSYIH15_GY_CF
TP_GSYIH16_GY_CF
"""


# pandas dataframe
df = get_series(template, cache=False)
print(df)


# Result Class instance
#   .data       : pd.DataFrame (data)        e.g. result.data
#   .metadata   : pd.DataFrame (metadata)    e.g. result.metadata
#   .write()    : Callable                   e.g. result.write("example.xlsx")
result = get_series_exp(template, cache=False)

print(result)  # Result
print(result.data)  # pd.DataFrame
print(result.metadata)  # pd.DataFrame

result.write("example.xlsx")
