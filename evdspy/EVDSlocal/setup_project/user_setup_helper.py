from evdspy.EVDSlocal.setup_project.user_series_config import quickNoteForParams


def add_indent(content):
    quickNoteForParamsLines = content.split("\n")
    quickNoteForParamsLines = (" " * 10 + x for x in quickNoteForParamsLines)
    content = "\n".join(quickNoteForParamsLines)
    return content


quickNoteForParams = add_indent(quickNoteForParams)
series_title = f"""#Series_config_file    
E V D S P Y  _  C O N F I G  _  F I L E  ---------------------------------------------
#
# This file will be used by evdspy package (python) in order to help updating 
# your series. 
# Script will be adding to it content when you setup a new project.
# Deleting this file current file may require to setup a new configuration from the beginning
#		please see `README.md` file 
# ----------------------------------------------------------------------------------------
#
#About alternative params 
# ----------------------------------------------------------------------------------------

{quickNoteForParams}
#Begin_series
"""
