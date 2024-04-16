
from dataclasses import dataclass
from rich import pretty
@dataclass
class CurrentState:
    """ Global State to check loaded functions
    and other global variables  """
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'):
            cls.instance = super(CurrentState, cls).__new__(cls)
            cls.set_state_on_load(cls)
            cls.set_result_dict(cls)
            cls.initial_sets(cls)
        return cls.instance
    def initial_sets(cls):
        cls.menu_will_open = False
    def set_state_on_load(cls, attr="loaded_menu_on_load", value=True):
        cls.loaded_menu_on_load = False
    def set_state(cls, attr="loaded_menu_on_load", value=True):
        cls.__setattr__(attr, value)
        # self.loaded_menu_on_load = False
    def set_result_dict(cls, attr=None, value=None):
        if attr is None:
            result = {}
            cls.result = result
        else:
            cls.result.update({attr: value})
    def get_result_dict(cls, id=None) -> [dict, any]:
        if id is None:
            result = cls.result
        else:
            result = cls.result.get(id, None)
        return result
    def __repr__(cls):
        return pretty.Pretty(cls.result)
        # return f"CurrentState:{cls.result}"