# from functools import lru_cache
import shutil

from ..common.common_imports import *
from evdspy.EVDSlocal.utils.utils_general import *
from ..components.api_params import get_enum_with_value
from ..components.options_class import load_options, SingletonOptions
from ..common.url_clean import remove_api_key
from evdspy.EVDSlocal.series_format.stats.save_stats_of_requests import Report
from evdspy.EVDSlocal.config.apikey_class import ApikeyClass
from typing import Union

# -----------------------------------------------------------------------------
test_result_file_name = str(get_current_dir() / ".." / "requests_" / "test_reg_result")
arg_sep = "_argSEP_"
p = Path()
pickle_folder = p.absolute() / 'pickles'


# -----------------------------------------------------------------------------


class CacheDecider(Enum):
    day = date.today()
    hour = datetime.now().strftime("%H")
    nocache = datetime.now().strftime("%H:%M:%S")
    default = date.today()


options_ = load_options()


def get_default_cache():
    obj = {
            "daily": CacheDecider.day,
            "hourly": CacheDecider.hour,
            'nocache': CacheDecider.nocache,
            'default': CacheDecider.day

    }
    return obj.get(options_.default_cache, CacheDecider.day)


def cache_represent(choice: CacheDecider):
    obj = {
            CacheDecider.day: "daily",
            CacheDecider.hour: "hourly",
            CacheDecider.nocache: 'nocache',
            CacheDecider.default: 'daily'
    }
    return obj[choice]


@dataclass
class MyCache:
    decider: Union[CacheDecider, None] = None  # post init

    # get_default_cache()  # get_default_cache()  # CacheDecider.hour
    report_ = Report("stats_requests.txt")

    def __post_init__(self):
        default_cache = SingletonOptions().get_valid_value("default_cache")
        self.decider = get_enum_with_value(key=default_cache, enum_=CacheDecider, default_value=CacheDecider.day)

    def update_rules_of_cache(self):
        if ApikeyClass().now_testing_is_key_is_valid:
            msg = "since this looks like a test, Program will be changing cache rulse to nocahce at all..."
            print(msg)
            deb(msg)

    def report(self, content=None):
        if content is None:
            content = f"""

            Cache Info : Current request cache method caches {cache_represent(self.decider)}

"""
        self.report_.add(content)

    def prepare_report_for_cache(self, func, args):
        self.report("Cache loaded...")
        str_args = (x for x in args if isinstance(x, str))
        str_args = tuple(map(remove_api_key, str_args))
        content = f"<function:{func.__name__}>" ", \n".join(str_args)
        self.report(content)

    def cache(self, func):
        self.update_rules_of_cache()

        @functools.wraps(func)
        def wrapper_decorator(*args, **kwargs):
            if self.check_cache(func, *args):
                value = self.load_cache(func, *args)
                self.prepare_report_for_cache(func, args)

            else:
                value = func(*args, **kwargs)
                self.save_cache(func, *args, data=value)
            return value

        return wrapper_decorator

    def sort_safe(self, items):
        items = list(items)
        items = sorted(items)
        return items

    def safe_serialize(self, *items):
        safe_list = []
        for item in items:
            if isinstance(item, str):
                safe_list.append(item)

        safe_list = self.sort_safe(safe_list) + [str(self.decider)]
        parameters = arg_sep.join(safe_list)
        return parameters

    def get_hash_alt1(self, st):
        import hashlib, base64
        d = hashlib.md5(bytes(st, encoding="utf-8")).digest()
        d = base64.urlsafe_b64encode(d).decode('ascii')
        return d

    def get_func_hash(self, f, *args):
        parameters = self.safe_serialize(*args)
        f_hash = f"{f.__name__}__{parameters}"
        f_hash = self.get_hash_alt1(f_hash)
        return f_hash

    def check_cache(self, f, *args):
        """added below to provide an exception when we check for valid key """
        self.update_rules_of_cache()

        f_hash = self.get_func_hash(f, *args)
        f_hash_path = rf"{pickle_folder}\\{f_hash}"
        return check_pickle(f_hash_path)

    def load_cache(self, f, *args):
        f_hash = self.get_func_hash(f, *args)
        f_hash_path = rf"{pickle_folder}\\{f_hash}"
        return load_pickle(f_hash_path)

    def save_cache(self, f, *args, data=None):
        f_hash = self.get_func_hash(f, *args)
        f_hash_path = f"{pickle_folder}\\{f_hash}"
        save_pickle(f_hash_path, data)


def check_pickle(file_name: str) -> bool:
    return os.path.isfile(file_name + ".pickle")


def load_pickle(file_name: str) -> Union[bool, requests.models.Response]:
    file_name = file_name + ".pickle"
    file_name_path = Path(file_name)

    if not file_name_path.is_file():
        print(file_name_path)
        return False
    with open(file_name_path, "rb") as infile:
        test_dict_reconstructed: requests.models.Response = pickle.load(infile)

        # exit()

    # f = bound(print, f"{file_name_path} pickle loaded...")
    # functools.partial(print, f"{file_name} pickle loaded...")
    # delay(1, f)
    msg = f"""
    
    ---------------------------------
    
    
    Recent cache was found for this request phrase.
    ---------------------------------
        It will be loaded instead of making a new redundant request 
        You may change cache options in options file.
    ---------------------------------
        cache loaded...({file_name_path})
"""

    print(msg)

    return test_dict_reconstructed


def delete_cache_folder():
    path = Path(pickle_folder)
    if not path.is_dir():
        return True
    try:
        # Path.rmdir(path)
        # os.remove(path)
        shutil.rmtree(path)
        return True
    except Exception as exc:
        print(exc)
    return False


def save_pickle(file_name, data):
    # print("saving", file_name)
    msg = f"""
        
    ---------------------------------
    
    
        Request was successfull...
        ---------------------------------
            Cache will be saved for this result. Next time program will be
            checking if this cache is new enough to load for the new request 
            You may change cache options in options file 
            ---------------------------------
            cache saved ...({file_name})
            
    """

    file_name_path = file_name + ".pickle"
    try:
        save_pickle_helper(file_name_path, data)
    except:

        print("Cache folder may be deleted.\n setup_now() inorder to create...")
        # if callable("setup_now"):
        #     setup_now()
        #     save_pickle_helper(file_name_path, data)


def save_pickle_helper(file_name_path, data):
    with open(file_name_path, "wb") as outfile:
        pickle.dump(data, outfile)
    f = bound(print, f"{file_name_path} pickle saved...")
    delay(1, f)


def save_pickle_for_test(data):
    save_pickle(test_result_file_name, data)


def load_test_pickle():
    return load_pickle(test_result_file_name)


def lru_cache_patched(maxsize=128, typed=False):
    import weakref
    def decorator(func):
        @functools.wraps(func)
        def wrapped_func(self, *args, **kwargs):
            self_weak = weakref.ref(self)

            @functools.wraps(func)
            @functools.lru_cache(maxsize=maxsize, typed=typed)
            def cached_method(*args, **kwargs):
                return func(self_weak(), *args, **kwargs)

            setattr(self, func.__name__, cached_method)
            return cached_method(*args, **kwargs)

        return wrapped_func

    if callable(maxsize) and isinstance(typed, bool):
        func, maxsize = maxsize, 128
        return decorator(func)
    return decorator


__all__ = [
        'lru_cache_patched',
        'MyCache',
        'save_pickle_for_test',
        'load_test_pickle'
]
