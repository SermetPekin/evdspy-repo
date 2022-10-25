from .cmd_formats import *
from ..common.common_imports import *
from ..common.files import Read, ReadBytes


def display_help_messages_md():
    def ReadLocal(filename: str):
        long_des = ""

        with open(filename, "r") as file_:
            long_des = file_.read()
        return long_des

    # return
    from rich.console import Console
    from rich.markdown import Markdown
    print(Path().parent)
    content_md = ReadLocal(str(Path() / Path().parent / "README.md"))
    console = Console()
    # print(content_md)
    md = Markdown(content_md)
    console.print(md)
    return content_md
    # content_md = str(content_md).encode('utf8')
    # md = Markdown(str(content_md))
    # console.print(md)


def display_help_messages():
    """ Some help to show some useful commands of project """
    ##############  commands #################
    msg = rf"""


--------importing -----
from evdspy  import *

-------------

------------ Below you may find some useful commands to check your installation of evdspy
             You may modify `IO\options.py` file with your preferences
                            `series.txt` file with your data series codes

menu() :
-------------
            Quickly setup your work environment run commands from the menu. \
            Currently you may choose one below or create your own functions and \
            add to this list following instructions on Readme.md
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
                           10. exit (from the menu)


10.exit (#Console#)
            Choosing 10 (Exit from the menu) you may continue working with commands summarized below
            or importing additional commands from the documentation. 
help_evds() :
-------------
    to see a list of initial commands  
    to check setup and reinitialize some installations.

check():
-------------
    see current installation status

easy_setup()   :
-------------
    # creates necessary folders such as `pickles`, `IO` for the environment

    easy_setup()
    
setup_steps()   :
-------------
    # this function helps you setup your project by asking your preferences step by step
    setup_steps()
    setup()

get():
-------------
    # this will check for your current series.txt file 
    # if proper data series codes are given it will either download them
    # or use latest cache from your local environment 
    # to provide other cache options such as nocache / daily / hourly you may change your 
    # defaults or give arguments such as 
        
        get(cache="daily")
        get(cache = "nocache")
        or to go with default from your option file 
        get()

save( key = "xxxxyyy"):
-------------
    # to get data quickly for this session you may set  apikey which will
    # be deleted before the session ends,  
    # if you would like to provide a file adress which has your api key 
    # see the other option setting your key globally 
    # => change your options.py file in IO folder 
    set_apikey("MyApiKey")
save():
-------------
    When you call it with not argument program will ask for your key and do the same 
    above 
create_series_file():
-------------
    # creates example `series.txt` evdspy input file (EIF) formatted 
    # you may modify it accordingly, you may user separator of -- between different groups  

    create_series_file()
    # or
    csf()

menu() :
-------------
            Quickly setup your work environment run commands from the menu. 
            Currently you may choose one below or create your own functions and 
            add to this list following instructions on Readme.md
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
                           10. exit (from the menu)\

-----------------------------------------------------------------------
# from evdspy import *         #(if you have not imported evdspy yet )
menu()                         # to see the menu() 
-----------------------------------------------------------------------
"""
    ############## END of commands #################

    ################ p r i n t ###############
    print(msg)
    ################            #######


from rich import print
from ..common.colors import *


def welcome_message():
    msg = f"""
    Welcome to evsdpy python interface...
    --------------------------------------------------------------------------------------------------
    This message appears when you use evdspy as a command line tool. 
    This welcome and help message will show up when you use `evdspy` command with no parameters...
    --------------------------------------------------------------------------------------------------
    Some parameters are listed below. If there is another command you are looking for you may check the menu option.
    
    $ evdspy --menu 
    --------------
        Loads the menu
        
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

    $ evdspy setup
    --------------
        creates initial folders for your environment to save data and caches 
        
    $ evdspy menu
    --------------
        Launces evdspy and loads the menu  
    $ evdspy save
    --------------
        asks for your api key to save a file in your environment named `APIKEY_FOLDER`

"""
    print_with_success_style(msg)
