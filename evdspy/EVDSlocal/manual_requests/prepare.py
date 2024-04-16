
from dataclasses import dataclass, field
from typing import List, Union, Tuple
from evdspy.EVDSlocal.messages.error_classes import ApiKeyNotSetError, SeriesEmptyError
from evdspy.EVDSlocal.config.config import config
from evdspy.EVDSlocal.requests_.real_requests import RealRequestWithParam
CANCEL_REQUEST_TEMP = config.cancel_request_temp
def test():
    p = PrepareUrl(series=('TP_ODEMGZS_NORVEC-8',), frequency=5, api_key='api_key')
    print(p.get_data())
from rich import print, inspect
def basic_for_test(api_key):
    url = "https://evds2.tcmb.gov.tr/service/evds/series=TP.ODEMGZS.BDTTOPLAM-TP.ODEMGZS.ABD-TP.ODEMGZS.ARJANTIN-TP.ODEMGZS.BREZILYA-TP.ODEMGZS.KANADA-TP.ODEMGZS.KOLOMBIYA-TP.ODEMGZS.MEKSIKA-TP.ODEMGZS.SILI&startDate=01-01-2019&endDate=01-12-2030&frequency=5&aggregationTypes=avg-avg-avg-avg-avg-avg-avg-avg&formulas=0-0-0-0-0-0-0-0&type=csv"
    # url = f"{url}&key={api_key}"
    req = RealRequestWithParam(url, api_key=api_key)
    response = req.request()
    # p_basic = PrepareUrl()
    # response = p_basic.get_data_with_url(url)
    return getattr(response, "status_code") and response.status_code in (200,)
def basic_for_testOLD(api_key):
    url = "https://evds2.tcmb.gov.tr/service/evds/series=TP.ODEMGZS.BDTTOPLAM-TP.ODEMGZS.ABD-TP.ODEMGZS.ARJANTIN-TP.ODEMGZS.BREZILYA-TP.ODEMGZS.KANADA-TP.ODEMGZS.KOLOMBIYA-TP.ODEMGZS.MEKSIKA-TP.ODEMGZS.SILI&startDate=01-01-2019&endDate=01-12-2030&frequency=5&aggregationTypes=avg-avg-avg-avg-avg-avg-avg-avg&formulas=0-0-0-0-0-0-0-0&type=csv"
    url = f"{url}&key={api_key}"
    p_basic = PrepareUrl()
    response = p_basic.get_data_with_url(url)
    return getattr(response, "status_code") and response.status_code in (200,)
def basic_for_test2(api_key):
    p_basic = PrepareUrl(
        series=('TP.ODEAYRSUNUM6.Q1',),
        api_key=api_key,
        frequency=5,
        basic=True)
    print(p_basic.get_data())
    url = p_basic.get_data()
    url = clean(url)
    print(url)
    return "WHAT"
    # make_request
    return p_basic.response.status_code in (200,)
def basic_test_with_real_key():
    real_api_key = ''
    return basic_for_test(real_api_key)
def clean(url):
    import string
    return url.translate({ord(c): None for c in string.whitespace})
default_start_date = "01-01-2019"
default_end_date = "01-01-2030"
@dataclass
class PrepareUrl:
    series: Tuple[str] = ()
    api_key: str = ""
    frequency: Union[int, None] = None
    aggregateType: Union[str, None] = "avg"
    basic: bool = False
    def get_data(self,
                 series=None,
                 api_key=None,
                 startDate=default_start_date,
                 endDate=default_end_date,
                 frequency=None,
                 aggregateType=None
                 ):
        if series is None:
            series = self.series
        if api_key is None:
            api_key = self.api_key
        if frequency is None:
            frequency = self.frequency
        if self.basic:
            self.create_url(
                series=series,
                api_key=api_key,
                startDate=startDate,
                endDate=endDate,
                frequency=frequency,
                aggregateType=aggregateType,
            )
        return self.get(
            self.create_url(
                series=series,
                api_key=api_key,
                startDate=startDate,
                endDate=endDate,
                frequency=frequency,
                aggregateType=aggregateType,
            ))
    def get(self, url):
        print(url)
        return url
    def get_data_with_url(self, url):
        return self.make_request(url)
    def series_to_str(self, series):
        return "-".join(series)
    def create_url(self, series, api_key, startDate, endDate, frequency, aggregateType):
        domain: str = "https://evds2.tcmb.gov.tr/service/evds/"
        if series is None:
            raise SeriesEmptyError
        if api_key is None:
            raise ApiKeyNotSetError
        if frequency is None and aggregateType is None:
            return f"{domain}series={self.series_to_str(series)}&startDate={startDate}&endDate={endDate}&type=csv&key={api_key}"
        if frequency:
            if aggregateType:
                return f"{domain}series={self.series_to_str(series)}" \
                       f"&frequency={frequency}" \
                       f"&aggregationTypes={aggregateType}" \
                       f"&type=csv" \
                       f"&key={api_key}"
            else:
                return f"{domain}series={self.series_to_str(series)}" \
                       f"&frequency={frequency}" \
                       f"&aggregationTypes=avg" \
                       f"&type=csv" \
                       f"&key={api_key}"
    def make_request(self, url=None):
        from ..messages.error_classes import ApiKeyNotSetError
        if url is None:
            url = self.url
        if CANCEL_REQUEST_TEMP:
            print("CANCEL_REQUEST_TEMP is True ...prepare.151")
            return False
        try:
            # self.response = requests.get(url)
            self.response = RealRequestWithParam(url).request()
        except ApiKeyNotSetError:
            ...
            return
        return self.response
import requests
def make_request(url: str):
    return requests.get(url)