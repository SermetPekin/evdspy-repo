
from dataclasses import dataclass, field
from enum import Enum
from evdspy.EVDSlocal.components.url_class import URLClass
class RequestType(Enum):
    Request = "request"
    Cache = "cache"
class RequestOrCacheResultInfo():
    safe_url: str = ""
    request_type: RequestType
    columns: tuple
    excel_saved: bool
    url_instance: URLClass
    def __init__(self, safe_url='', request_type=RequestType.Request, columns=(), excel_saved=False, url_instance=None):
        self.safe_url = safe_url
        if request_type is None:
            request_type = RequestType.Request
        if url_instance is None:
            url_instance: URLClass = field(default_factory=URLClass)  # URLClass([])
        self.request_type = request_type
        self.columns = columns
        self.excel_saved = excel_saved
    def get_data(self):
        content = f"""
url : {self.safe_url}
request or cache : {self.request_type.value}
columns : {self.columns}
excel file was saved ? : {self.excel_saved}
"""
        return content
# @dataclass
# class RequestOrCacheResultInfo():
#     safe_url: str = ""
#     request_type: RequestType = field(default=RequestType.Request)
#     columns: field(default_factory=tuple) = field(default_factory=tuple)
#     excel_saved: bool = False
#     url_instance: URLClass = URLClass(())
#
#     def get_data(self):
#         content = f"""
# url : {self.safe_url}
# request or cache : {self.request_type.value}
# columns : {self.columns}
# excel file was saved ? : {self.excel_saved}
# """
#         return content