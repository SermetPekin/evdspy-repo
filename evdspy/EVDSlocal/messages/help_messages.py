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
    from .current_menu_message import current_menu_appears

    """ Some help to show some useful commands of evdspy package """
    ##############  commands #################
    msg = rf"""


--------importing -----
from evdspy  import *

-------------

menu() :
-------------
            Quickly setup your work environment run commands from the menu. \
            Currently you may choose one below or create your own functions and \
            add to this list following instructions on Readme.md
${current_menu_appears}


help_evds() :
-------------
    to see a list of initial commands  
    to check setup and reinitialize some installations.

check():
-------------
    see current installation status
    
setup()   :
-------------
    # this function helps you setup your project by asking your preferences step by step
    setup() 
get():
-------------
    # this will check for your current config_series.cfg file 
    # if proper data series codes are given it will either download them
    # or use latest cache from your local environment 
    # to provide other cache options such as nocache / daily / hourly you may change your 
    # defaults or give arguments such as 
        
        get(cache="daily")
        get(cache = "nocache")
        or to go with default from your option file 
        get()

save("MyApiKey" ):
-------------
    # saves your api key to use while requesting data from the server.\
    # creates an APIKEY_FOLDER and saves some hash function of your api key for security.
    # If you are on a public computer we suggest you delete this folder when you are done requesting data.
    
    save("MyApiKey")

save():
-------------
    When you call it with not argument program will ask for your key and do the same 
    above 
create_series_file():
-------------
    # creates example `config_series.cfg` evdspy input file (EIF) formatted 
    # you may modify it accordingly, you may user separator of `--++--` between different series groups  

    create_series_file()
    # or
    csf()

menu() :
-------------
    
Quickly setup your work environment run commands from the menu. 
Currently you may choose one below or create your own functions and 
add to this list following instructions on Readme.md
${current_menu_appears}

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
    This message appears when you use evdspy as a command line prompt. 
    This welcome and help message will show up when you use `evdspy` command with no parameters...
    --------------------------------------------------------------------------------------------------
    Some parameters are listed below. If there is another command you are looking for you may check the menu option.
    
    $ evdspy setup
    --------------
        creates initial folders for your environment to save data and caches 
        
    $ evdspy menu 
    --------------
        Loads the menu
        
    $ evdspy create series  
    --------------
        Creates series file (leaves untouched if exists)       
        
    $ evdspy create options
    --------------
        creates options on the current folder 
        
    $ evdspy save
    --------------
        asks for your api key to save a file in your environment named `APIKEY_FOLDER`
        
    $ evdspy get
    --------------
        makes request from EVDS API and creates excel files regarding information on your series file 
        
    $ evdspy help
    --------------
        shows help and some documentation from command line 
"""
    print_with_success_style(msg)
