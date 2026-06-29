import pandas as pd

from evdspy import get_series_exp
from evdspy.EVDSlocal.index_requests.get_series_indexes_exp import Result

index1 = "TP.GSYIH20.BY.B1GQ"
index2 = "TP.GSYIH20.BY.P311"

indexes = """ 
TP.GSYIH20.BY.B1GQ	     # Gayrisafi Yurt İçi Hasıla (Harcama Yöntemiyle, Cari Fiyatlarla)-Düzey		
TP.GSYIH20.BY.P311       # Yerleşik Hanehalklarının Tüketimi (Harcama Yöntemiyle, Cari Fiyatlarla)-Düzey		
TP.GSYIH20.BY.P312       # Hanehalkına Hizmet Eden Kar Amacı Olmayan Kuruluşların Tüketimi (Harcama Yöntemiyle, Cari Fiyatlarla)-Düzey		
TP.GSYIH20.BY.P32        # Devletin Nihai Tüketim Harcamaları (Harcama Yöntemiyle, Cari Fiyatlarla)-Düzey		
TP.GSYIH20.BY.P51G	     # Gayrisafi Sabit Sermaye Oluşumu (Harcama Yöntemiyle, Cari Fiyatlarla)-Düzey		
TP.GSYIH20.BY.P52	     # Stoktaki Değişiklikler (Harcama Yöntemiyle, Cari Fiyatlarla)-Düzey		
TP.GSYIH20.BY.P6	     # Mal ve Hizmet İhracatı (Harcama Yöntemiyle, Cari Fiyatlarla)-Düzey		
TP.GSYIH20.BY.P7         # (Eksi) Mal ve Hizmet İthalatı (Harcama Yöntemiyle, Cari Fiyatlarla)-Düzey		

"""
index_table = "bie_gsyhhrccar"


from typing import Any
import time


def fnc(item: Any) -> Result:
    print(f"  Checking ...  {item}")
    time.sleep(2)
    df = get_series_exp(item, debug=False, cache=True)
    print(df)
    return df


DF = pd.DataFrame

def test_get_series_exp(capsys):
        items = [index1, index2, indexes, index_table]

        for item in items:
            result: Result = fnc(item)

            assert isinstance(result.data, DF)
            assert isinstance(result.metadata, DF)
            assert callable(result.write)
            assert callable(result.to_excel)
            
