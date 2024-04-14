from evdspy.EVDSlocal.utils.utils_general import *
from evdspy.EVDSlocal.series_format.series_format_config_funcs import *

mainSepBegin = "---Series---------------------------------"
mainSepEnd = "---/Series---------------------------------"
GSEP = "--++--"
NEW_LINE = "\n"
example_codes = ['TP.EVDSSTATS.KAYITLI', 'TP.EVDSSTATS.ZIYARET']
example_codes_str = ",".join(example_codes)

# ----------------------------- S E R I E S ---------------------------------------------------
items_from_user_series = [
        "Data folder",
        "Subject",
        "Name prefix(Optional) Default : `EVPY_` ",
        "EVDS data series codes",
        "Frequency",
        "Formulas",
        "AggregateType",
]

default_prefix = "EVPY_"
freq = f"""
Daily: 1
Business: 2
Weekly(Friday): 3
Semimonthly: 4
Monthly: 5
Quarterly: 6
Semiannual: 7
Annual: 8
"""
frequency_dict = {
        1: 'Daily',
        2: 'Business day',
        3: 'Weekly(Friday)',
        4: 'Semimonthly',
        5: 'Monthly',
        6: 'Quarterly',
        7: 'Semiannual',
        8: 'Annual',
}
default_freq = "5"
formulas_ = f"""
Level: 0
Percentage change: 1
Difference: 2
Year-to-year Percent Change: 3
Year-to-year Differences: 4
Percentage Change Compared to End-of-Previous Year: 5
Difference Compared to End-of-Previous Year : 6
Moving Average: 7
Moving Sum: 8
"""
formulas_dict = {
        0: "Level",
        1: "Percentage change",
        2: "Difference",
        3: "Year-to-year Percent Change",
        4: "Year-to-year Differences",
        5: "Percentage Change Compared to End-of-Previous Year",
        6: "Difference Compared to End-of-Previous Year",
        7: "Moving Average",
        8: "Moving Sum",
}
default_formulas_ = "0"
AggregateType_ = f"""
Average: avg,
Minimum: min,
Maximum: max
Beginning: first,
End: last,
Cumulative: sum
"""
quickNoteForParams = f"""
Frequencies
-----------------
{freq}
`Formulas`s
-----------------
{formulas_}
Aggregate types
-----------------
{AggregateType_}
"""
AggregateType__valid_answers = ["avg", "min", "max", "first", "last", "sum"]
default_AggregateType_ = "avg"
explanations_series = [
        rf"Path for your project {NEW_LINE}{indent}(Example: output or C:\Users\Userx\MyTempData ) default: {default_prefix}Data "
        rf"{NEW_LINE} This should be an empty folder. If folder does not exist"
        "program will create a new folder with this name",
        rf"Subject will be used to name excel files. {NEW_LINE}{indent}(Example: Visitors, Tourism, Balance of Payments, Exchange Rates etc.",
        "If there is already excel files in the folder this will prevent replacing existing files.  ",
        rf"evdspy will create your series.txt file {NEW_LINE} it will add data series codes if you provide. "
        rf"{NEW_LINE} {indent} example : {example_codes_str} {NEW_LINE}"
        f"You may also continue with default values and modify the config_series.cfg file later if you prefer",
        f"{freq}\nFrequency (Number between 1, 8  e.g.(monthly) : 5) default: 1",
        f"{formulas_}\n e.g. (Number between 0, 8  e.g.(Level) : 0) default: 0 ",
        f"{AggregateType_}\n e.g. ( avg / min / max / first / last / sum  ) default: avg",
]


def check_valid_answer(items, answer: str):
    return answer in items


def check_valid_answer_freq(answer: str):
    return check_valid_answer(tuple(map(str, range(1, 8))), answer) or answer.strip() == ""


def check_valid_answer_formulas_(answer: str):
    return check_valid_answer(tuple(map(str, range(0, 9))), answer) or answer.strip() == ""


def check_valid_answer_aggr(answer: str):
    return check_valid_answer(AggregateType__valid_answers, answer) or answer.strip() == ""


default_answer_subject = 'SubjectNotGiven'
default_answers_series = [f"{default_prefix}Data",
                          default_answer_subject,
                          default_prefix,
                          example_codes,
                          default_freq,
                          default_formulas_,
                          default_AggregateType_]
check_funcs_series = [folder_format_check,
                      TrueFunc,
                      TrueFunc,
                      TrueFunc,
                      check_valid_answer_freq,
                      check_valid_answer_formulas_,
                      check_valid_answer_aggr]
# import string
# x = "aa,ab-ac"
# s = x.split()
#
""" Transform Functions """
same = lambda x: x
trim_string = lambda x: x.strip()
from typing import Tuple

# import re
# split_items = lambda x: re.split("[,-/\n;]+", x)
split_items = lambda text: tuple(text.translate(text.maketrans({x: "-" for x in "[,-/\n;]~"})).split("-"))
""" Default answers if the user goes with an Empty answer """


def get_default_for_question(answer, question):
    obj = {
            "folder": f"{default_prefix}Data",
            "prefix": default_prefix,
            "freq": default_freq,
            "formulas": default_formulas_,
            "aggr": default_AggregateType_,
            "series": example_codes,
            "subject": default_answer_subject
    }
    if not answer.strip():
        """ default returns here """
        return obj.get(question, answer)

    if question == "series":
        """item1,item2\nitem3"""
        return split_items(answer)
    return answer.strip()


# instead of functools partial lambda this time
bound_question = lambda question: lambda answer: get_default_for_question(answer, question)
funcs_names = ("folder", "subject", "prefix", "series", "freq", "formulas", "aggr",)
transform_answers_series: Tuple = tuple(map(lambda x: bound_question(x), funcs_names))
