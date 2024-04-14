from evdspy.EVDSlocal.common.colors import print_with_info_style
from evdspy.EVDSlocal.config.config import config

width = 60


def make_indent(element, num=width):
    indent = " " * (num - len(element))
    return f"{indent}{element}"


def make_center(element, num=width):
    left = " " * round((num - len(element)) / 2)
    return f"{left}{element}"


def menu_header(self):
    menu_title = make_center("M E N U")
    reminder = "to get the latest version:   pip install -U evdspy"
    reminder = make_indent(reminder)
    version_line = make_indent(config.version)
    logo = make_indent("evdspy @2022")
    line_1 = "-" * width
    print_with_info_style(reminder)
    header = f"""

{line_1}
{version_line}  
{line_1}   
{logo} 
{menu_title}                      
{line_1}
"""
    return header


def version_logo():
    # menu_title = make_center("M E N U")
    reminder = "for the latest version: pip install -U evdspy"
    reminder = make_indent(reminder)
    version_line = make_indent(config.version, 15)
    logo = make_indent("evdspy @2022", 30)
    line_1 = "-" * width

    logo_version = f"""
    {line_1}
  {logo}  {" " * 5} {version_line}  
    {line_1}   
    
    """

    logo_version2 = f"""
    {line_1}
    {version_line}  
    {line_1}   
    {logo} 
    """

    return logo_version, reminder
