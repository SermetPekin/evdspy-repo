from evdspy import *

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

df = get_series(template, debug=False)
print(df)


