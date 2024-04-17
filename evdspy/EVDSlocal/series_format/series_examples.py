
site_visitors = rf"""
#Series_config_file
E V D S P Y  _  C O N F I G  _  F I L E  ---------------------------------------------
#
# This file will be used by evdspy package (python) in order to help updating
# your series.
# Script will be adding this file when you setup a new project.
# Deleting or modifying its content may require to setup configuration from the beginning
# ----------------------------------------------------------------------------------------
#
#About alternative params
# ----------------------------------------------------------------------------------------
          Frequencies
          -----------------
          Daily: 1
          Business: 2
          Weekly(Friday): 3
          Twicemonthly: 4
          Monthly: 5
          Quarterly: 6
          Semiannual: 7
          Annual: 8
          `Formulas`s
          -----------------
          Level: 0
          Percentage change: 1
          Difference: 2
          Year-to-year Percent Change: 3
          Year-to-year Differences: 4
          Percentage Change Compared to End-of-Previous Year: 5
          Difference Compared to End-of-Previous Year : 6
          Moving Average: 7
          Moving Sum: 8
          Aggregate types
          -----------------
          Average: avg,
          Minimum: min,
          Maximum: max
          Beginning: first,
          End: last,
          Cumulative: sum
#Begin_series
---Series---------------------------------
foldername : visitors/annual
abs_path : visitors/annual # will check again before saving requests from the server it might be replaced by ...WD.../DataSeries/visitors\monthly
subject  : visitors
prefix   : EVPY_
frequency : 8 # annually
formulas : 0 # Level
aggregateType : avg
------------SERIES CODES------------------
TP.ODEMGZS.BDTTOPLAM
TP.ODEMGZS.ABD
TP.ODEMGZS.ARJANTIN
TP.ODEMGZS.BREZILYA
TP.ODEMGZS.KANADA
TP.ODEMGZS.KOLOMBIYA
TP.ODEMGZS.MEKSIKA
TP.ODEMGZS.SILI
------------/SERIES CODES------------------
---/Series---------------------------------
--++--
---Series---------------------------------
foldername : visitors/monthly
abs_path : visitors/monthly # will check again before saving requests from the server it might be replaced by ...WD.../DataSeries/visitors\monthly
subject  : visitors
prefix   : EVPY_
frequency : 5 # Monthly
formulas : 0 # Level
aggregateType : avg
------------SERIES CODES------------------
TP.ODEMGZS.BDTTOPLAM
TP.ODEMGZS.ABD
TP.ODEMGZS.ARJANTIN
TP.ODEMGZS.BREZILYA
TP.ODEMGZS.KANADA
TP.ODEMGZS.KOLOMBIYA
TP.ODEMGZS.MEKSIKA
TP.ODEMGZS.SILI
------------/SERIES CODES------------------
---/Series---------------------------------
--++--
"""
test_series_file_content_for_test = site_visitors
example_series = [site_visitors]
__all__ = [
        'example_series',
]