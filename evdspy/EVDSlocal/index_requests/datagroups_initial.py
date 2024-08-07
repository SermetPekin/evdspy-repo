
from .index_classes import GeneralIndexesDatagroups
from .data_models import DataModelCSV, DataModelJSON
from ..components.options_class import SingletonOptions
from ..requests_.ev_request import EVRequest
# GID_csv = lambda x: GeneralIndexesDatagroups().get_csv
# GID_json = lambda x: GeneralIndexesDatagroups().get_json
data_strategy = {"csv": GeneralIndexesDatagroups(EVRequest_=EVRequest(options_=SingletonOptions())).get_csv,
                 "json": GeneralIndexesDatagroups().get_json}
data_models_dict = {"csv": DataModelCSV, "json": DataModelJSON}