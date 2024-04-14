from evdspy.EVDSlocal.components.evds_seri_files import EvdsSeri, EvdsSeriesRequest, EvdsSeriesRequestWrapperFromFile, \
    BucketFromSeriesFile
from evdspy.EVDSlocal.messages.error_classes import *
from evdspy.EVDSlocal.common.files import *
from evdspy.EVDSlocal.series_format.populate_series_helper import *

# from evdspy.EVDSlocal.series_format.series_creator import get_approval

NEW_LINE = "\n"
GSEP = "--++--"
BeginS = "#Begin_series"
series_begins_note = "---Series - --------------------------------"

from evdspy.EVDSlocal.messages.error_messages import *

from typing import Callable

from evdspy.EVDSlocal.config.config import config
from evdspy.EVDSlocal.series_format.series_examples import test_series_file_content_for_test
from evdspy.EVDSlocal.initial.start_options import *

from evdspy.EVDSlocal.series_format.series_examples import example_series


def get_input(msg):
    if config.current_mode_is_test:
        return "test"
    ans = input(msg)
    return str(ans)


def get_approval(file_name):
    msg = f"{file_name} already exists. If you would like to replace it with a new example please type `replace`: "

    ans = get_input(msg)
    if str(ans).lower().strip() == "replace":
        return True
    return False


def create_series_text_file(file_name: str, content=""):
    """General usage"""
    if Path(file_name).is_file() and "-locked" not in file_name.lower():
        if not get_approval(file_name):
            return False
    print(f"creating...{file_name}")
    result, msg = Write(file_name, content)
    print(msg)
    time.sleep(1)
    return result


import random


def create_series_text_example(file_name=default_series_file_name):
    """ main series config file """
    return create_series_text_file(file_name, random.choice(example_series))


@dataclass
class PopulateSeries:
    name: str = "config_series.cfg"
    separator: str = GSEP
    EvdsSeriesRequestWrapper_Type: Callable = EvdsSeriesRequestWrapperFromFile
    injection: bool = False  # for pytest

    def __post_init__(self):
        self.input_file_name = Path() / f"{self.name}"
        if not self.input_file_name.is_file():
            create_series_text_example()
        self.checks()

    def checks(self):

        items_will_be_checked = (
            BeginS in self.series_file_full_content and self.separator in self.series_file_full_content,
            self.series_file_full_content.count(
                series_begins_note) < self.series_file_full_content.count(
                self.separator)
            ,)

        if not all(items_will_be_checked):
            ...
            msg = f"{self.input_file_name} may be corrupted. You may create a new one from the menu. (create series config file)"
            print(msg )
            raise SeriesFileDoesNotExists(msg)

        deb(f"reading :  {self.input_file_name}", f"content: {self.series_file_content}")
        deb(f"content: {self.series_file_content}")

    def extract_group(self, group: str):
        return [x for x in group.split(NEW_LINE) if x != '']

    @property
    def series_file_full_content(self):
        if config.current_mode_is_test:
            return test_series_file_content_for_test

        content = Read(self.input_file_name)
        return content

    @property
    def series_file_content(self):
        if self.injection:
            return self.injected_content
        self.full_content = content = self.series_file_full_content
        if BeginS in self.full_content:
            content = self.full_content.split(BeginS)[1]
        return content

    def check_file(self):
        x = self.input_file_name.is_file()
        if not x:
            print(SeriesFileDoesNotExists(series_file_not_found_error_msg))
            return x
        return x

    def split_series_file(self, content=None):
        """ main function to split content from series file"""
        if content is None:
            """ For pytest or other test processes """
            content = self.series_file_content
        else:
            self.injection = True
            self.injected_content = content
        groups = content.split(self.separator)

        conts = [self.extract_group(group) for group in groups]
        conts = [cont for cont in conts if len(cont) > 1]
        return [self.create_class(cont) for cont in conts]

    def create_class(self, cont):
        def check(x):
            return all(("#" not in x, "--" not in x, ":" not in x, len(x) > 2))

        folder_name = self.extract_prop(cont, "foldername")
        abs_path = self.extract_prop(cont, "abs_path")
        subject = self.extract_prop(cont, "subject")
        prefix = self.extract_prop(cont, "prefix")
        frequency = self.extract_prop(cont, "frequency")
        formulas = self.extract_prop(cont, "formulas")
        aggregateType = self.extract_prop(cont, "aggregateType")

        bfs = BucketFromSeriesFile(folder_name=folder_name,
                                   subject=subject,
                                   prefix=prefix,
                                   frequency=frequency,
                                   formulas=formulas,
                                   aggregateType=aggregateType,
                                   abs_path=abs_path)

        series_codes = [x for x in cont if check(x)]
        objs = [EvdsSeri(x, bfs=bfs) for x in series_codes]

        # def update(item: EvdsSeri):
        #     item.bfs = bfs
        #
        #     return item
        #
        # objs: List[EvdsSeri] = [update(x) for x in objs]

        return self.export_series(objs, bfs)

    def export_series(self, objs, bfs: BucketFromSeriesFile):
        req = EvdsSeriesRequest(series_list=objs, bfs=bfs)

        assert self.EvdsSeriesRequestWrapper_Type is EvdsSeriesRequestWrapperFromFile, "populate 82"
        return self.EvdsSeriesRequestWrapper_Type(bfs=bfs, EvdsSeriesRequest_=req)

    def clean_series_line(self, line):
        line = line.strip()
        line = line.split("#")
        return line[0]

    def extract_prop(self, lines, prop):
        def get_prop(prop, item):
            value = ""
            r = item.split(":")
            if len(r) > 2:
                # "folder:http:xx"
                value = ":".join(r[1:])
            elif len(r) > 1:
                # "filename:xx"
                value = r[1]
            return value.strip()

        lines = [self.clean_series_line(x) for x in lines if ":" in x]
        lines = [get_prop(prop, x) for x in lines if prop in x]
        lines = [x for x in lines if x is not None]
        if len(lines) == 0:
            lines = ["prop_not_found"]
        return lines[0]

    def process(self):
        reqs = self.split_series_file()
        return reqs


__all__ = [
    'PopulateSeries',

]


# req = PopulateSeries().split_series_file()
# print(req )

def check_pop_read():
    ps = PopulateSeries()
    req = ps.split_series_file(content=pop_series_test_content)
    deb2(req)
    return req
