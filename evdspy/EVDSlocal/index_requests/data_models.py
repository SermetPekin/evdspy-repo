from abc import ABC
from dataclasses import dataclass


@dataclass
class DataModel(ABC):
    data: any
    type_name: str = ""


@dataclass
class DataModelCSV(DataModel):
    type_name: str = "csv"


@dataclass
class DataModelJSON(DataModel):
    type_name: str = "json"
