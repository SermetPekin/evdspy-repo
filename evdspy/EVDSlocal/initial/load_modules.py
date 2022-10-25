# -------------------------------------------------------------------------
# from evdspy.EVDSlocal.before_main_ import *
from evdspy.EVDSlocal.components.evds_files import EvdsSorguSeries
from evdspy.EVDSlocal.components.evds_seri_files import EvdsSeri, EvdsSeriesRequest, EvdsSeriesRequestWrapper
from evdspy.EVDSlocal.series_format.populate_series import PopulateSeries
from evdspy.EVDSlocal.series_format.series_creator import SeriesFileFormat, create_series_file_from_Wrapper, \
    create_series_text_file
from evdspy.EVDSlocal.initial.start_args import Args
from evdspy.EVDSlocal.components.options_class import *
from evdspy.EVDSlocal.components.evds_seri_files import test_series_
from ..initial_setup.setup_folders import check_setup
from ..messages.error_classes import *
from evdspy.EVDSlocal.log_classes.log_template import deb
from evdspy.EVDSlocal.config.config import ConfigBase

from evdspy.EVDSlocal.manual_requests.prepare import basic_for_test, PrepareUrl

from evdspy.EVDSlocal.config.apikey_class import ApikeyClass


@dataclass
class LoadModulesClass():
    options_: Optional[any] = load_options()
    args: Optional[Args] = Args(sys.argv)
    evds_list: field(default_factory=list) = ()
    series_filename: str = default_series_file_name
    api_key_test: bool = False
    # TODO
    """
    """

    def placebo_item(self):
        evds = EvdsSorguSeries(
            options_=self.options_,
            session=None,
            subject="placebo",
            series_=test_series_,
            file_name="placebo",
            args=self.args)
        return evds

    def summary(self):
        if not self.evds_list or not len(self.evds_list) > 0:
            print("No EvdsSorguSeries yet")
            return
        for item in self.evds_list:
            item.summary()

    def series_from_file_test(self):
        """Reads series' code from given file name inside initial folder default :`series.txt` """
        return self.create_EVDSSorguSeries()

    def main(self):
        return self.series_from_file()

    def series_from_file(self):
        """ MAIN function """
        result = []
        try:
            result = self.series_from_file_core()
        except SeriesFileDoesNotExists:
            print(SeriesFileDoesNotExists().message)

        return result

    def convert_wrapperlist_to_text(self, wrapper_list: List[EvdsSeriesRequestWrapper]):
        content = create_series_file_from_Wrapper(wrapper_list)
        return content

    def create_locked_series_file(self):
        wrapper_list = self.populate_evds_wrapperList()
        content = self.convert_wrapperlist_to_text(wrapper_list)
        file_name = default_series_file_name.split(".cfg")[0] + "-locked.cfg"
        create_series_text_file(file_name, content)

    def create_EVDSSorguSeries(self):
        return self.populate_evds_list()

    def populate_evds_wrapperList(self):
        # return
        # if self.api_key_test:
        #     """ api key already was tested here we are checking if it is valid """
        #     self.series_filename = str(
        #         ConfigBase().runtime_file_name_root_path / "series_format" / "series_test_runtime.cfg")
        #     # self.series_filename = "series_format/series_test_runtime.cfg"
        sff = SeriesFileFormat(self.series_filename)
        return sff.EvdsSeriesRequestWrapperList

    def check_for_apikey_with_simple_wrapper(self, api_key):

        basic_for_test(api_key)
        exit()

        self.api_key_test = True
        self.evds_list = self.populate_evds_list()
        if not self.evds_list:
            return False
        self.evds_list = [self.evds_list[0]]
        return self.evds_to_excel(api_key_test=True)

        # return len(evds_list) and isinstance(evds_list[0], EvdsSorguSeries)

    def populate_evds_list(self):
        """==>>>>   (Deep )   PopulateSeries() =>
                    (Surface) SeriesFileFormat .EvdsSeriesRequestWrapper_
        Reads series' code from given file name
        inside initial folder default :`series.txt`
        returns a list of wrapper
        ( EvdsSeriesRequestWrapper1 ,  EvdsSeriesRequestWrapper2 , ... )
        EvdsSeriesRequestWrapper :
            name
            subject
            EvdsSeriesRequest
        """
        list_ = []
        EvdsSeriesRequestWrapperList = self.populate_evds_wrapperList()
        for index, EvdsSeriesRequestWrapper_ in enumerate(EvdsSeriesRequestWrapperList):
            evds = EvdsSorguSeries(
                options_=self.options_,
                session=None,
                subject=EvdsSeriesRequestWrapper_.subject,
                series_=EvdsSeriesRequestWrapper_.EvdsSeriesRequest_,
                file_name=EvdsSeriesRequestWrapper_.name,
                args=self.args,
                bfs=EvdsSeriesRequestWrapper_.bfs,
            )

            list_.append(evds)
        return list_

    def evds_to_excel(self, api_key_test=False):
        for evds in self.evds_list:
            try:

                evds.save_excel()
                evds.report()
            except Exception as exc:
                # print(exc)
                # print(evds)
                deb(str(exc))

        return True

    def series_from_file_core(self):
        self.evds_list = self.create_EVDSSorguSeries()
        self.evds_to_excel()
        self.create_locked_series_file()
        return True

    def seri_ornek(self, options_, args):
        liste = [
            'TP.IHRACATBEC.9999',
            'TP.IHRACATBEC.31',
            'TP.IHRACATBEC.41',
        ]
        seri_evds_objs: list[EvdsSeri] = [EvdsSeri(x) for x in liste]
        series_ = EvdsSeriesRequest(self.options_, seri_evds_objs)
        file_name = "test34"
        evds = EvdsSorguSeries(
            session=None,
            series_=series_,
            file_name=file_name
        )
        evds.save_excel(evds.file_name)

    def check(self):
        evds_items = self.series_from_file_test()
        if len(evds_items):
            self.check_items(evds_items)

    def check_items(self, evds_items):
        config = ConfigBase()
        options_copy_file_name = config.runtime_file_name_path
        user_options_file_name = config.user_options_file_name
        deb(config)
        # args = Args(sys.argv)
        ps = PopulateSeries()
        series_file_was_created = False
        f = Path(ps.input_file_name)
        if f.is_file():
            series_file_was_created = True

        folders_ok = False
        if check_setup():
            folders_ok = True
        api_key_is_ok = False
        if ApikeyClass().get_valid_api_key():
            api_key_is_ok = True

        def display():
            options_file_name = "options.cfg"
            options_file_created = Path(options_file_name).is_file()
            options_display = SingletonOptions().check()

            hiddenok = f"ok(hidden)"
            if not api_key_is_ok:
                hiddenok = ""
            msg = f"""
        Checking installation and other setup requirements :
        ----------------------------------------------------
        Folders created          :      {folders_ok}
        Series file was created  :      {series_file_was_created} {indent} {ps.input_file_name}
        Options file was created :      {options_file_created} {indent} {options_file_name}
        Api key was set          :      {api_key_is_ok} {indent} {hiddenok}
        {options_display}
                """
            print(msg)

        display()