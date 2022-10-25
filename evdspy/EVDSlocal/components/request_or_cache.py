from dataclasses import dataclass, field
from enum import Enum
from evdspy.EVDSlocal.components.url_class import URLClass
class RequestType(Enum):
    Request = "request"
    Cache = "cache"
@dataclass
class RequestOrCacheResultInfo():
    safe_url: str = ""
    request_type: RequestType = RequestType.Request
    columns: field(default_factory=tuple) = tuple()
    excel_saved: bool = False
    url_instance: URLClass = URLClass([])
    def get_data(self):
        content = f"""
url : {self.safe_url}
request or cache : {self.request_type.value}
columns : {self.columns}
excel file was saved ? : {self.excel_saved}
"""
        return content
