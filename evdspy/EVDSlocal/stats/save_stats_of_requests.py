from evdspy.EVDSlocal.common.files import *
from dataclasses import dataclass, field

from datetime import datetime


@dataclass
class Report:
    file_name: str = "stats_report.txt"

    @property
    def date_content(self):
        now = datetime.now()

        current_time = now.strftime("%Y-%m-%d %H:%M:%S")
        return current_time

    def add(self, content):
        content = f"{self.date_content} => {content}"
        WriteAdd(self.file_name, content)


def report_test():
    r = Report(file_name="test_stats_report.txt")
    r.add("content")