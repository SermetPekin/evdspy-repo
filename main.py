import pandas as pd

from evdspy import get_series, get_series_exp


# The `get_series` function extracts the series ticket from the input string
# by using only the initial characters that match the expected ticket format,
# ignoring any trailing or unrelated characters.

template = """
TP.KKO2.IS.TOP 
TP.KKO2.IS.S2	 
TP.KKO2.IS.S3	# İmalat Sanayi Kapasite Kullanım Oranı _ BG3-Düzey
TP.KKO2.IS.S4	# İmalat Sanayi Kapasite Kullanım Oranı _ BG4-Düzey
TP.KKO2.IS.CDUR	    Dayanıklı Tüketim Malları-Düzey
TP.KKO2.IS.CNDU    	Dayanıksız Tüketim Malları-Düzey
TP.KKO2.IS.CONS	Tüketim Malları-Düzey
TP.KKO2.IS.FOBE	Gıda ve içecekler-Düzey
TP.KKO2.IS.INTM	Ara Malları-Düzey
TP.KKO2.IS.INVE	Yatırım Malları-Düzey
TP.KKO2.IS.10	# 10_Gıda ürünlerinin imalatı-Düzey
TP.KKO2.IS.11	#11_İçeceklerin imalatı-Düzey
TP.KKO2.IS.12	12_Tütün ürünleri imalatı-Düzey
TP.KKO2.IS.13	13_Tekstil ürünlerinin imalatı-Düzey
TP.KKO2.IS.14	14_Giyim eşyalarının imalatı-Düzey
TP.KKO2.IS.15	15_Deri ve ilgili ürünlerin imalatı-Düzey
TP.KKO2.IS.16	16_Ağaç, ağaç ürünleri ve mantar ürünleri imalatı (mobilya hariç)-Düzey
TP.KKO2.IS.17	17_Kağıt ve kağıt ürünlerinin imalatı-Düzey
TP.KKO2.IS.18	18_Kayıtlı medyanın basılması ve çoğaltılması-Düzey
TP.KKO2.IS.19	19_Kok kömürü ve rafine edilmiş petrol ürünleri imalatı-Düzey
TP.KKO2.IS.20	20_Kimyasalların ve kimyasal ürünlerin imalatı-Düzey
TP.KKO2.IS.21	21_Temel eczacılık ürünlerinin ve eczacılığa ilişkin malzemelerin imalatı-Düzey
TP.KKO2.IS.22	22_Kauçuk ve plastik ürünlerin imalatı-Düzey
TP.KKO2.IS.23	23_Diğer metalik olmayan mineral ürünlerin imalatı-Düzey
TP.KKO2.IS.24	24_Ana metal sanayii-Düzey
TP.KKO2.IS.25	25_Fabrikasyon metal ürünleri imalatı (Makine ve teçhizat hariç)-Düzey
TP.KKO2.IS.26	26_Bilgisayarların, elektronik ve optik ürünlerin imalatı-Düzey
TP.KKO2.IS.27	27_Elektrikli teçhizat imalatı-Düzey
TP.KKO2.IS.28	28_Başka yerde sınıflandırılmamış makine ve ekipman imalatı-Düzey
TP.KKO2.IS.29	29_Motorlu kara taşıtı, treyler (römork) ve yarı treyler (yarı römork) imalatı-Düzey
TP.KKO2.IS.30	30_Diğer ulaşım araçlarının imalatı-Düzey
TP.KKO2.IS.31	31_Mobilya imalatı-Düzey
TP.KKO2.IS.32	32_Diğer imalatlar-Düzey
TP.KKO2.IS.33	33_Makine ve ekipmanların kurulumu ve onarımı-Düzey

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
