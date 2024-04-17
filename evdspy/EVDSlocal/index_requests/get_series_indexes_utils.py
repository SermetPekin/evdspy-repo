
from enum import Enum
from typing import Optional, Union, Any
def default_start_date_fnc():
    return "01-01-2000"
def default_end_date_fnc():
    return "01-01-2100"
class AggregationType(Enum):
    """
    avg : "avg"
    min : "min"
    max : "max"
    first : "first"
    last : "last"
    sum : "sum"
    """
    avg = "avg"
    min = "min"
    max = "max"
    first = "first"
    last = "last"
    sum = "sum"
    def __str__(self):
        return self.value
class Formulas(Enum):
    """Formulas
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
    level = 0
    percentage_change = 1
    difference = 2
    year_to_year_percent_change = 3
    year_to_year_differences = 4
    percentage_change_compared = 5
    difference_compared = 6
    moving_average = 7
    moving_sum = 8
    def __str__(self):
        return self.value
    @classmethod
    def from_str(cls, string: str):
        """Converts a string to a corresponding enum member."""
        mapping = {
            "level": cls.level,
            "percentage change": cls.percentage_change,
            "difference": cls.difference,
            "year to year percent change": cls.year_to_year_percent_change,
            "year to year differences": cls.year_to_year_differences,
            "percentage change compared": cls.percentage_change_compared,
            "difference compared": cls.difference_compared,
            "moving average": cls.moving_average,
            "moving sum": cls.moving_sum
        }
        normalized_string = string.lower().replace("_", " ").strip()
        if normalized_string in mapping:
            return mapping[normalized_string]
        else:
            raise ValueError(f"Unknown formula type: {string}")
class Frequency(Enum):
    daily = 1
    business = 2
    weekly = 3  # Friday
    semimonthly = 4
    monthly = 5
    quarterly = 6
    semiannually = 7
    annual = 8
    annually = 8
    def __str__(self):
        return self.value
    def __call__(self, *args, **kwargs):
        return f"&frequency={self.value}"
def freq_enum(frequency: Union[str, int]) -> str:
    def get_enum(value: str):
        obj = {
            "daily": Frequency.daily,
            "business": Frequency.business,
            "weekly": Frequency.weekly,
            "semimonthly": Frequency.semimonthly,
            "monthly": Frequency.monthly,
            "quarterly": Frequency.quarterly,
            "semiannually": Frequency.semiannually,
            "annual": Frequency.annually,
            "annually": Frequency.annually,
        }
        return obj.get(str(value).lower(), Frequency.daily)
    if isinstance(frequency, int):
        return f"&frequency={frequency}"
    return get_enum(frequency)()
def correct_types(value: Optional[tuple], enum_class) -> Union[str, int, tuple ]:
    if value is None: return value
    # first_type = type(next(iter(enum_class)).value)
    if isinstance(value, tuple):
        return tuple(map(lambda x: correct_types(x, enum_class), value))
    if isinstance(value, enum_class):
        return value.value
    if isinstance(value, str) and hasattr(enum_class, "from_str"):
        return enum_class.from_str(value).value
    else:
        return value