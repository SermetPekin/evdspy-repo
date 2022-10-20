from .help_messages import *
from .cmd_formats import *

api_key_not_set_msg = f"""
        ---------------------------------------------------------------        
               WARNING
        ---------------------------------------------------------------
        Api key not set . 
        you may continue with saving your api key by answering 
                 `yes` 
        Program will store your api key in a private area and read it when 
        it needs to request data from EVDS server. 
        You may get your api key from your EVDS account on EVDS website.
        
        Note : Alternatively you may continue with providing a text file 
        address that contains your api key. 
        (Please choose `provide api key file` option for this option.)
    
"""
you_need_to_run_setup_options = f"""
    it looks like options.py not created.
    try command below from command line in your project's root folder.

{setup_now_command}
        

"""

copying_options_msg = "Found an options file... Trying to copy it to temporary env."

series_file_not_found_error_msg = f""" 
create_series_file

"""
