from .help_messages import *
from .cmd_formats import *

api_key_not_set_msg = f"""
        ---------------------------------------------------------------        
               WARNING
        ---------------------------------------------------------------
        Api key not set . 
        ---------------------------------------------------------------
        you may continue with saving your api key by answering 
                 `yes` 
        
        Program will store your api key in your work environment creating a folder `APIKEY_FOLDER` and read it when 
        it needs to request data from EVDS server. 
        
        This key will be used when you run your requests and will be saved to your work environment 
        in a folder named APIKEY_FOLDER in a text file not as a plane text but in a obscured way. 
        If you are working in a public workspace we suggest that you delete this folder once you are finished making requests.
        Program will not use or store your API key to any other folder therefore when you delete, remove or rename this folder 
        program will ask your API key again.
        
        Below, there are links of the institution's web service. Signing up or logining in you may find your API key on 
        your account. 
        
        You may get your api key from your account on CBRT EVDS website.
        
        CBRT EVDS API (TCMB EVDS API)
        -----------------

        Sign up / Log in
        https://evds2.tcmb.gov.tr/index.php?/evds/login
        Main page 
        https://evds2.tcmb.gov.tr
        Docs 
        https://evds2.tcmb.gov.tr/index.php?/evds/userDocs
        
        If you already have an API key may continue with saving your api key by answering 
                 `yes` now and then your API key"""
you_need_to_run_setup_options = f"""
    it looks like options.py not created.
    try command below from command line in your project's root folder.

{setup_now_command}
        

"""

copying_options_msg = "Found an options file... Trying to copy it to temporary env."

series_file_not_found_error_msg = f""" 
create_series_file

"""
