
# ------------------------------------------------------------------------------
import pandas as pd
from evdspy.EVDSlocal.initial.start_options import default_series_file_name
from evdspy.EVDSlocal.config.config import *
from evdspy.EVDSlocal.components.excel_class import *
from ..requests_.request_error_classes import Internal
from ..utils.utils_general import *
from ..requests_.my_cache import MyCache
from ..components.options_class import Options, load_options
from ..components.evds_seri_files import EvdsSeriesRequest, test_series_
from evdspy.EVDSlocal.requests_.ev_request import EVRequest
from ..config.credentials_file import Credentials
from ..initial.start_args import *
from ..config.apikey_class import *
from dataclasses import dataclass
from typing import Union, List, Tuple
from ..common.colors import *
# ------------------------------------------------------------------------------
m_cache = MyCache()
number = 0
# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
# /*
#               EvdsSorgu
#
# ------------------------------------------------------------------------------
# */
from evdspy.EVDSlocal.components.evds_seri_files import BucketFromSeriesFile
from evdspy.EVDSlocal.components.request_or_cache import RequestOrCacheResultInfo
from evdspy.EVDSlocal.state.current_state import CurrentState
from evdspy.EVDSlocal.components.url_class import URLClass
from evdspy.EVDSlocal.components.api_params import Series, DateStart, DateEnd
current_state = CurrentState()
class DfColumnsDoesNotMatch(BaseException):
    """DfColumnsDoNotMatch"""
from evdspy.EVDSlocal.messages.error_classes import ApiKeyNotSetError
# field(default_factory=URLClass)
@dataclass
class EvdsSorgu(ABC):
    """ EVDS Genel SÃ„Â±nÃ„Â±f"""
    options_: Options
    session: any
    series_: EvdsSeriesRequest = field(
        default_factory=EvdsSeriesRequest)  # field(default=test_series_)  # None  # test_series_
    file_name: Optional[str] = "test"
    subject: str = "test_subject"
    df: any = None
    excel_out_ext: str = "xlsx"
    args: Args = field(default_factory=Args)  # Args(sys.argv)
    url: Optional[str] = None
    proxy: Optional[str] = False
    bfs: BucketFromSeriesFile = None
    df_checked: bool = False
    request_or_cache_resultInfo_: RequestOrCacheResultInfo = field(default_factory=RequestOrCacheResultInfo)
    def __post_init__(self):
        # self.URL_Instance = URLClass()
        self.credentials = field(default_factory=Credentials)  # Credentials(options_=self.options_)
        self.address: str = ''  # field(default=self.credentials.address)
        self.EVRequest_: EVRequest = field(default_factory=EVRequest)  # EVRequest(options_=self.options_, session=None)
        self.parent_folder = Path(__file__).parent
        self.core_file_name = self.file_name
        self.file_name = str(Path().absolute() / "output" / self.file_name)
        self.current_file_created = ""
        self.display()
        self.assign_results_to_state()
        if not self.check_api_key_first():
            print_with_failure_style("Api key")
    def assign_results_to_state(self):
        """
        save result stats to state
            to finally access from bfs
        """
        current_state.set_result_dict(str(id(self.bfs)), self.request_or_cache_resultInfo_)
    def report(self):
        m_cache.report()
        ...
    def display(self, *args):
        # global number
        # number += 1
        items_series = (x.ID for x in self.series_.series_list)
        dec = f"""
----------------------------------------
    Order item from '{default_series_file_name}'
    Details :
    bfs : {self.bfs}
___________________
    filename: {self.core_file_name}
    subject : {self.subject}
    series :
        {", ".join(items_series)}
----------------------------------------
"""
        print(dec)
        return dec
    def check_api_key_first(self):
        # TODO  ApikeyClass().get_valid_api_key()
        if not self.EVRequest_:
            self.EVRequest_ = EVRequest(options_=load_options(),
                                        session=None,
                                        proxy=None,
                                        args=Args(())
                                        )
        try:
            if ApikeyClass().get_valid_api_key():
                # self.EVRequest_.check_any_apikey()
                return True
        except ApiKeyNotSetError:
            return False
    def create_url(self):
        api_key = ApikeyClass().get_valid_api_key()
        if not config.current_mode_is_test:
            assert api_key is not False, "api_key is False "
        self.complete_url_instance: URLClass = self.series_.complete_url_instance
        self.request_or_cache_resultInfo_.url_instance = self.series_.complete_url_instance
        self.complete_url_instance.refresh_url()
        self.request_or_cache_resultInfo_.safe_url = f"{self.complete_url_instance.create_report()}"
        will_be_requested: Tuple = (
            self.complete_url_instance.url,
            self.complete_url_instance.url_only_required,
        )
        return will_be_requested
    def get_json(self, url: str):
        """ Not implemented """
        raise NotImplementedError
        # return self.EVRequest_.get_request_before_cache(f"{url}&type=json").json()
    def get_csv(self, url: str):
        if not hasattr(self.EVRequest_, 'URL_Instance'):
            self.EVRequest_ = EVRequest(options_=load_options())
            self.EVRequest_.URL_Instance = URLClass()
        self.EVRequest_.URL_Instance = self.complete_url_instance
        result = self.EVRequest_.get_request_before_cache(f"{url}&type=csv")
        if hasattr(result, "text"):
            self.csv = result.text
            return result.text
        return False
    @staticmethod
    def extract_values_from_line(line: str, sep=","):
        return line.split(sep)
    @staticmethod
    def line_gen(buffer: str):
        if not buffer:
            return False
        for item in buffer.split("\n"):
            yield item
    # @staticmethod
    def get_columns_from_first_row(self):
        first_row = self.csv.split("\n")[0].split(",")
        return first_row
    def get_columns(self, df):
        current_columns = df.columns  # rangeIndex
        if isinstance(current_columns, pd.RangeIndex):
            current_columns_len = len([x for x in current_columns])
        else:
            current_columns_len = len(current_columns)
        potential_columns = self.get_columns_from_first_row()
        if len(potential_columns) != current_columns_len:
            raise DfColumnsDoesNotMatch()
        df.columns = self.get_columns_from_first_row()
        self.request_or_cache_resultInfo_.columns = df.columns
        UnixTime = 'UNIXTIME'
        if UnixTime in df.columns:
            df.drop(UnixTime, axis=1, inplace=True)
        if config.current_mode_is_test:
            self.save_excel("testpytest2.xlsx")
        return df
    @staticmethod
    def list_to_df(items):
        return pd.DataFrame(items)
    def make_df_float(self):
        def check_cols(x: str):
            items = (
                "Tarih" not in x,
                "WEEK" not in x,
                "DAY" not in x,
            )
            return all(items)
        columns = (x for x in self.df.columns if check_cols(x))
        other_cols = (x for x in self.df.columns if not check_cols(x))
        old_df = self.df
        try:
            self.df = self.df[columns].astype(float)
            for other_column in other_cols:
                self.df[other_column] = old_df[other_column]
        except:
            print_with_failure_style("Could not convert some columns to float type...")
    def convert_csv_df(self, csv_buffer: str):
        if not csv_buffer:
            return False
        pd_rows = list(
            map(self.extract_values_from_line,
                (item for item in self.line_gen(csv_buffer))
                )
        )
        pd_rows.pop(0)
        self.df_no_columns = self.list_to_df(pd_rows)
        try:
            self.df = self.get_columns(self.df_no_columns)
        except DfColumnsDoesNotMatch:
            print_with_failure_style("columns did not match returning df with no columns...")
            self.df = self.df_no_columns
            print(self.df.head())
            filename = "error_" + str(id(self.df)) + ".xlsx"
            # self.df.to_excel(filename)
            print_with_info_style("error: requested URL does not fit...")
            time.sleep(1)
            return False
        except Exception as e:
            print_with_failure_style(e)
            pass
        self.make_df_float()
        return self.df
    @property
    def got_items(self):
        if not self.check_api_key_first():
            return False
        self.df_checked = True
        return self.get_items_csv()
    def get_items_csv(self):
        will_be_requested = self.create_url()
        for item in will_be_requested:
            try:
                df = self.convert_csv_df(self.get_csv(item))
            except DfColumnsDoesNotMatch:
                continue
            except Internal:
                continue
            if isinstance(df, pd.DataFrame):
                return df
        return False
    def get_items_json(self):
        """not implemented"""
        # return self.convert_csv_df(self.get_json(self.create_url()))
    def save_excel(self, file_name=None):
        deb("not writing... evds_files. 175")
        return True
#   ----------------------------------------------------------    / EvdsSorgu
# ------------------------------------------------------------------------------
# /*
#               EvdsSorguSeries
#
# ------------------------------------------------------------------------------
# */
@dataclass
class EvdsSorguSeries(EvdsSorgu):
    """ Seriler iÃƒÂ§in """
    def summary(self):
        if not self.check_api_key_first():
            return False
        self.df = self.got_items
        if not isinstance(self.df, pd.DataFrame):
            return False
        # print(self.df.head())
        return self.df.head()
    def save_excel(self, file_name=None):
        if not self.df_checked:
            self.df = self.got_items
        file_name = self.bfs.xls_name_path
        try:
            os.makedirs(self.bfs.abs_path)
        except:
            pass
        # assert file_name == "ttt"
        if not isinstance(self.df, pd.DataFrame):
            print_with_failure_style("df was not created")
            self.request_or_cache_resultInfo_.excel_saved = False
            return
        self.ExcelSaveClass_ = ExcelSaveClass(self.df, file_name)
        self.ExcelSaveClass_.save_excel__()
        self.request_or_cache_resultInfo_.excel_saved = True
        return True
#   ----------------------------------------------------------    / EvdsSorguSeries
__all__ = [
    'EvdsSorguSeries',
    'EvdsSorgu',
]