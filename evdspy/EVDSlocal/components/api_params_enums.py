import typing as t
from enum import Enum, auto


# ------------------------------------------------------- E N U M S -------------------------------------------------------

class EnumBase(Enum):
    ...

# --------------------------------FrequencyEnum---------------------
class FrequencyEnum(Enum):
    daily = 1
    business_day = 2
    weekly = 3
    semimonthly = 4
    monthly = 5
    quarterly = 6
    semi_annual = 7
    annual = 8
    default = 5


# --------------------------------DomainParts---------------------

class DomainParts(Enum):
    categories = auto()
    datagroup = auto()
    series = auto()


# --------------------------------AggregationEnum---------------------

class AggregationEnum(Enum):
    average = "avg"
    min = "min"
    max = "max"
    first = "first"
    last = "last"
    cumulative = "sum"
    default = "avg"


# --------------------------------ModeEnumDatagroup---------------------

class ModeEnumDatagroup(Enum):
    all_groups = 0
    data_group = 1
    subject_group = 2
# --------------------------------CodeEnumDatagroup---------------------

# class CodeEnumDatagroup(Enum):
#     code_int = 1
#
#     data_group = 1
#     subject_group = 2


# --------------------------------Separator---------------------

class Separator(Enum):
    period = "."
    comma = ","


# --------------------------------dataTypeEnum---------------------

class dataTypeEnum(Enum):
    csv: str = "csv"
    json_type: str = "json"


# --------------------------------FormulasEnum---------------------

class FormulasEnum(Enum):
    level = 0
    percentage_change = 1
    difference = 2
    yoy_percentage_change = 3
    yoy_difference = 4
    per_cha_com_end_of_pre_yea = 5
    dif_com_end_of_pre_yea = 6
    moving_average = 7
    moving_sum = 8
    default = 0

    # ------------------------------------------------------- get_enum_with_value -------------------------------------------------------
    """ typical usages
        get_enum_with_value( 5 , Frequency , Frequency.Monthly )

    """


"""
        key: t.Union[Enum, str, int],
        # enum_: t.Union[str, int, t.Callable , Enum ],
        enum_: Enum,
        default_value: t.Union[str, int, t.Callable] = None
        
                key: t.Union[Enum, str, int],
        # enum_: t.Union[str, int, t.Callable , Enum ],
        enum_: any,
        default_value: any = None
"""


def get_enum_with_value(
        key: t.Union[Enum, str, int],
        enum_: t.Union[str, int, t.Callable , Enum ],
        # enum_: Enum,
        default_value: t.Union[str, int, t.Callable , Enum ] = None

) -> Enum :
    """

    :rtype: object
    """
    if isinstance(key, Enum):
        return key
    if isinstance(key, int):
        key = str(key)

    if hasattr(default_value, "value"):
        """otherwise probably None """
        default_value = getattr(default_value, "value", None)

    dd = {str(x.value): x for x in enum_}
    enum_value: Enum = dd.get(key, None)

    if hasattr(enum_value, "value"):
        v = getattr(enum_value, "value")
        return v
    if not default_value:
        return getattr(default_value, "default")
    return default_value
# ------------------------------------------------------- / get_enum_with_value -------------------------------------------------------
