
[![Python package](https://github.com/SermetPekin/evdspy-repo/actions/workflows/python-package.yml/badge.svg)](https://github.com/SermetPekin/evdspy-repo/actions/workflows/python-package.yml) [![PyPI](https://img.shields.io/pypi/v/evdspy)](https://img.shields.io/pypi/v/evdspy) [![Supported Python Versions](https://img.shields.io/pypi/pyversions/evdspy)](https://pypi.org/project/evdspy/) [![Downloads](https://pepy.tech/badge/evdspy/week)](https://pepy.tech/project/evdspy)
## Documentation
[Documentation](https://evdspy-repo.readthedocs.io/en/latest/)
## evdspy
### Updated on this version
    * The API key parameter has been moved to the HTTP header as required by recent updates from EDDS data provider.
    This change enhances security by ensuring that sensitive information is not exposed in URLs.
    * `get_series` function was added
    * [soon will be deprecated] **get_datagroup** function will be depreciated in the future versions.
    **get_series** function will be able to handle both series and datagroups.
> ! get_series function can be used for both datagroups and series
### api_key
api_key will be saved to a file if it was given to get_series function. It will ignore
later calls if it was saved before.
Alternatively save function can be used.
#### save("MyApiKey"):
    Program will store your api key in your environment in a safe folder
    called APIKEY_FOLDER
    and only use it when you run a new request which was not requested
    recently depending on your cache preference.
.
```python
from evdspy import save
save("MyApiKey")
```
```python
from evdspy import get_series, default_start_date_fnc, default_end_date_fnc
# datagroup `bie_gsyhgycf`
df1 = get_series("bie_gsyhgycf", cache=False, api_key="YOUR_API_KEY_HERE")
# series    `TP_GSYIH01_GY_CF ...`
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
df2 = get_series(template, debug=False, cache=False)
```
```python
from evdspy import get_series, default_start_date_fnc, default_end_date_fnc
index1 = "TP.ODEMGZS.BDTTOPLAM", "TP.ODEMGZS.ABD"
index2 = """
    TP.ODEMGZS.BDTTOPLAM #
    TP.ODEMGZS.ABD #
    """
cache = True
df = get_series(index1,
                frequency="monthly",
                start_date=default_start_date_fnc(),
                end_date=default_end_date_fnc(),
                aggregation=("avg",),
                cache=cache,
                debug=False)
print(df)
```
### Some more examples
```python
from evdspy import get_series
template = '''
    TP.ODEMGZS.BDTTOPLAM
    TP.ODEMGZS.ABD
    TP.ODEMGZS.ARJANTIN
    '''
df = get_series(index=template)
df1 = get_series(index=template, start_date="01-01-2000", frequency="monthly")
df2a = get_series(index='TP.ODEMGZS.BDTTOPLAM', start_date="01-01-2000", frequency="monthly", cache=True)
df2b = get_series(index=('TP.ODEMGZS.BDTTOPLAM', 'TP.ODEMGZS.ARJANTIN',),
                  start_date="01-01-2000",
                  frequency="monthly",
                  cache=True)
df3 = get_series(template, start_date="01-01-2000", frequency="monthly", aggregation="avg")
df4 = get_series(template, start_date="01-01-2000", frequency="monthly", aggregation=("avg", "min", "avg"))
df5 = get_series(template, proxy="http://proxy.example.com:80")
df6 = get_series(template, proxies={
    'http': "http://proxy.example.com:80",
    'https': "http://proxy.example.com:80",
})
```
## get_series
all parameters of get_series function
```python
from typing import Union
import pandas as pd
def get_series(
        index: Union[str, tuple[str]],
        start_date: str = '01-01-2000',
        end_date: str = '01-01-2100',
        frequency: str = None,  # | monthly | weekly | annually | semimonthly | semiannually | business
        formulas: str = None,  # | level | percentage_change | difference |
        #   | year_to_year_percent_change | year_to_year_differences |
        aggregation: str = None,  # | avg      |min    | max    | first    | last    |    sum
        cache: bool = False,
        proxy: str = None,
        proxies: dict = None,
        debug: bool = False
) -> pd.DataFrame:
    ...
"""proxy
proxy = "http://proxy.example.com:80"
"""
"""proxies
proxies = {
            'http':  "http://proxy.example.com:80",
            'https':  "http://proxy.example.com:80",
        }
"""
```
### Menu
```python
from evdspy.main import menu
menu()
```
![image](https://user-images.githubusercontent.com/96650846/198966008-77302f42-f8f5-430c-962d-a988abe57bb7.png)
## Visual Menu to request data
![image](https://user-images.githubusercontent.com/96650846/200393634-6d1d95cc-6fb5-4f2a-aff8-f444265df814.png)
![image](https://user-images.githubusercontent.com/96650846/200393889-915a1908-bff9-41fc-b549-d83b1cf9dafd.png)
### About
***evdspy*** is an open source python interface which helps you make efficient requests by caching results (storing a
dict using hashable parameters in order to avoid redundant requests), it provides a user friendly
menu to ask data from the institution's API service.
It is a Python interface to make requests from (CBRT) EVDS API Server. Fast, efficient and user friendly solution.
Caches results to avoid redundant requests. Creates excel files reading configuration text file that can be easily
created from the menu or console. Provides visual menu to the user. It is extendable and importable for user's own
python projects.
#### [Please see the disclaimer below](#Disclaimer)
### installation
    pip install evdspy
### importing
    from evdspy import *
    check()
    get()
    help_evds()
or
    import evdspy as ev
    ev.check()
    ev.get()
    ev.help_evds()
### menu
    from evdspy import *
    menu()
or
    import evdspy as ev
    ev.menu()
    Menu function will display a friendly menu to setup project, creating output folders and some setup files to
    create some set of series to make a request and download from EVDS server save your api key to get data from EVDS.
    Than it will convert this data to a pandas dataframe and create some folders on your local area.
### menu()
![image](https://user-images.githubusercontent.com/96650846/198966008-77302f42-f8f5-430c-962d-a988abe57bb7.png)
![image](https://user-images.githubusercontent.com/96650846/198966318-35a8ba8b-68e9-46f9-827e-cf06377ec960.png)
## OPTION 1
_________________________________
#### FROM THE CONSOLE
    create_series_file()
or
    csf()
or from selection menu choose create series file (config_series.cfg) option.
With this command program will create file similar to below. You may later add new series info
or modify this file or delete and create a new on from menu or console using commands summarized in this file.
#### config_series.cfg content example
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
    foldername : visitors\annual
    abs_path : visitors\annual
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
    foldername : visitors\monthly
    abs_path : C:\Users\User\SeriesData\visitors\monthly
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
### initial commands
    from evdspy import *
#### help_evds():
    see a list of popular commands of this package to create setup folder and files, and request data.
        'easy_setup',
    'setup',
    'setup_series',
    "setup_series_steps",
    'help_evds',
    'check',
    'get',
### help
    'h',
    'help_evdspy',
    'help_',
### series file
    'create_series_file',
    'csf',
### options file
    'create_options_file',
    'cof'
### menu , console
    'console',
    'menu',
### version
    'version',
### api key
    'save_apikey',
    'save',
### cache
    'remove_cache',
#### check():
    check setup and create required folders and see current installation status.
#### setup()   :
    creates folders and files
    ____Folders_______________
            `pickles`
                will be used to store some request results to ovoid redundant requests from the EVDS api
            `SeriesData`
                to save results of requests or caches to an excel file using information on user option files
    ____Files_______________
            `options.cfg`
                a text file consisting global user options such as start date, end date and caching period.
            `config_series.cfg`
                this file consists information regarding individual sets of series. From the menu user can add
            new series that will be requesting from the server. Program will produce on for example and this file
            can be modified and new sets of series can be added following the example format.
    from evdspy.main import *
    setup_now()
#### get():
    # this will check for your current series.txt file
    # if proper data series codes are given it will either download them
    # or use the latest cache from your local environment
    # to provide other cache options such as nocache / daily / hourly you may change your
    # defaults or give arguments such as
        get()
#### save("MyApiKey"):
    Program will store your api key in your environment in a safe folder
    called APIKEY_FOLDER
    and only use it when you run a new request which was not requested
    recently depending on your cache preference.
.
       save("MyApiKey")
#### save()
        When you call it without any argument, program will ask for your key and do the same
    above
#### create_series_file()  or csf() :
--------------------------------
    # creates example `config_series.cfg` file on your work environment. evdspy input file (EIF) formatted
    # you may modify it according to your preferences.
--------------------------------
    create_series_file()
    # or
    csf()
## Options File
-------------------------------------------------------------------
          #Global Options File (options.cfg)
          # G L O B A L   O P T I O N S   F I L E   -------------------------------------------------------
          cache_freq : daily
          gl_date_start : 01-01-2010
          gl_date_end : 01-12-2030
### `create_options`
    create_options()
## OPTION 2
_________________________________
#### FROM THE MENU
### menu()
![image](https://user-images.githubusercontent.com/96650846/198966008-77302f42-f8f5-430c-962d-a988abe57bb7.png)
> > *checking*....
![image](https://user-images.githubusercontent.com/96650846/200316924-de6c5d4c-e9d1-4122-a49b-45e1a4b5923b.png)
## OPTION 3
_________________________________
#### FROM THE OS COMMAND LINE
(Windows Command line / Linux Terminal / Mac Terminal) ( > , $ , $ as $ )
![image](https://user-images.githubusercontent.com/96650846/198182696-c5bbe840-a9cd-45b5-806f-ee9b7d0e88b8.png)
    $ evdspy setup
    --------------
        creates initial folders for your environment to save data and caches
    $ evdspy menu
    --------------
        Launces evdspy and loads the menu
    $ evdspy create series
    --------------
        Creates series file (leaves untouched if exists)
    $ evdspy help
    --------------
        shows help and some documentation from command line
    $ evdspy create options
    --------------
        creates options on the current folder
    $ evdspy get
    --------------
        makes request from EVDS API and creates excel files regarding information on your series file
    $ evdspy save
    --------------
        asks for your api key to save a file in your environment named `APIKEY_FOLDER`
## How to get an API key?
***Get a CBRT EVDS API key***
https://evds2.tcmb.gov.tr/index.php?/evds/login
#### Main page of CBRT EVDS API
https://evds2.tcmb.gov.tr
#### CBRT EVDS API Docs
https://evds2.tcmb.gov.tr/index.php?/evds/userDocs
### About
***evdspy*** is an open source python interface which helps you make efficient requests by caching results (storing a
dict using hashable parameters in order to avoid redundant requests), it provides a user friendly
menu to ask data from the institution's API service.
#### Disclaimer
    We would like inform you that evdspy is not an official package affiliated or endorsed by the CBRT institution.
    It is an open source project with MIT LICENSE therefore following the rules of its
    general MIT LICENSE you may use this interface without creator's permission, extend it or write your own modules
    by importing evdspy's modules, classes or functions to request data from the mentioned API Service following the
    institution's rules and parameters.