
[![Python package](https://github.com/SermetPekin/evdspy/actions/workflows/python-package.yml/badge.svg)](https://github.com/SermetPekin/evdspy/actions/workflows/python-package.yml)
[![Python 3.8](https://img.shields.io/badge/python-3.8-blue.svg)](https://www.python.org/downloads/release/python-380/)
[![Python 3.9](https://img.shields.io/badge/python-3.9-blue.svg)](https://www.python.org/downloads/release/python-390/)
[![Python 3.10](https://img.shields.io/badge/python-3.10-blue.svg)](https://www.python.org/downloads/release/python-310/)


## evdspy

### installation

    pip install evdspy

### importing

    from evdspy import *  
    check()
    get()
    help_evds()

or

    import evdspy as ev 
    eeev.check()
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

**************************************************

                    M E N U

**************************************************

               1. check setup
               2. setup
               3. create user options file
               4. create series file
               5. add new series group
               6. get data
               7. help
               8. show api key
               9. save api key to file
               10. console
    ......................... Selection ? 

#### FROM THE CONSOLE
### cache choice (default:daily)

    # hourly :  no new request within an hour with same URL combination
    # nocache: new request upon each call without checking cache results
    # daily : program will use local data requested earlier if data was saved same day.    

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

    from evdspy.main import * 

#### help_evds():

    see a list of popular commands of this package to create setup folder and files, and request data.
    

#### check():
    check setup and create required folders and see current installation status.

#### setup_now()   :

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


#### save( key = "xxxxyyy"):

    Program will store your api key in your environment in a safe folder
    called APIKEY_FOLDER
    and only use it when you run a new request which was not requested 
    recently depending on your cache preference.

.

       save_apikey("MyApiKey")

#### save()

        When you call it with not argument program will ask for your key and do the same 
    above 

#### create_series_file()  or csf() :

--------------------------------

    # creates example `config_series.cfg` file on your work environment. evdspy input file (EIF) formatted 
    # you may modify it according to your preferences.  

--------------------------------

    create_series_file()
    # or
    csf()

# MENU
### menu()

**************************************************

                    M E N U

**************************************************

               1. check setup
               2. setup
               3. create user options file
               4. create series file
               5. add new series group
               6. get data
               7. help
               8. show api key
               9. save api key to file
               10. exit (from menu to console)
    ......................... Selection ?