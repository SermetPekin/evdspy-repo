from evdspy.EVDSlocal.utils.utils_general import *
from evdspy.EVDSlocal.series_format.series_format_config_funcs import *

mainSepBegin = "---Series---------------------------------"
mainSepEnd = "---/Series---------------------------------"
GSEP = "--++--"
NEW_LINE = "\n"

# "cache_freq gl_date_start gl_date_end"

# ----------------------------- C O N F I G  ---------------------------------------------------
items_from_user_config = [
    "Cache frequency",
    "global date start for series",
    "global date end for the series",
    "avoid absolute paths protection" ,
]

explanations_config = [
    f"Cache frequency will be used to decide to make a new request. {NEW_LINE} "
    f"If recent cache is found in local cache folder program will use it instead of making a request. {NEW_LINE}"
    f" {indent} Options : monthly / daily / nocache. Default : daily {NEW_LINE}",
    f"if not special start date for the series was given in `config_series.cfg` file "
    f"this date will be used as start date of series {NEW_LINE} Example 19-01-2015",
    f"if not special end date for the series was given in `config_series.cfg` file "
    f"this date will be used as end date of series {NEW_LINE} Example : 19-01-2030",
    rf"if set False it will accept absolute paths such as C:\Users\Userx . default is True to protect users other folders from polluting"
]
check_funcs_options = [TrueFunc, TrueFunc, TrueFunc, TrueFunc]
default_answers_config = ['', '', '', 'True']
same = lambda x: x

transform_answers_options = (same for _ in items_from_user_config)
