# from evdspy.EVDSlocal.index_requests.user_requests import UrlSeries, UrlDataGroup
from evdspy.EVDSlocal.index_requests.user_requests.Request_config import RequestConfig


# ....................................................................... UrlBuilder
class UrlBuilder:
    def __init__(self,
                 config: RequestConfig,
                 url_type=None) -> None:
        self.config = config
        self.series_part = self.config.create_series_part()
        if not url_type:
            self.get_url_type()
        self.alias = self.url_type.alias

    def get_url_type(self):
        from evdspy.EVDSlocal.index_requests.user_requests import UrlSeries, UrlDataGroup
        url_type = UrlSeries()
        if self.config.check_type() == "datagroup":
            url_type = UrlDataGroup()
        self.url_type = url_type

    def create_url_for_series(cls) -> str:
        domain = cls.domain
        return f"{domain}/{cls.alias}{cls.series_part}&startDate={cls.config.start_date}&endDate={cls.config.end_date}&type=json"

    @property
    def domain(self) -> str:
        return self.url_type.domain

    @property
    def basic_url(self) -> str:
        config = self.config
        return f"{self.domain}/{self.alias}{self.series_part}&startDate={config.start_date}&endDate={config.end_date}&type=json"

    @property
    def url(self) -> str:
        config = self.config
        if config.frequency is None and config.aggregation is None and config.formulas is None:
            return self.basic_url
        """ config parts """
        formulas_str = config.formulas_to_str()
        aggregation_type_str = config.aggregation_type_to_str()
        freq_string = config.freq_str()
        """..."""
        parts = (
            f"{self.domain}/{self.alias}{self.series_part}{freq_string}{formulas_str}{aggregation_type_str}",
            f"startDate={config.start_date}",
            f"endDate={config.end_date}",
            "type=json"
        )
        return "&".join(parts)


# Implementation of HelpUrlBuilder
class HelpUrlBuilder:

    def __init__(self, config: RequestConfig, url_type=None) -> None:
        self.config = config
        self.index = self.clean(self.config.initial_index)
        # self.series_part = self.config.create_series_part()
        if not url_type:
            self.get_url_type()
        self.alias = self.url_type.alias

    def __str__(self):
        return f"""
    ........................... HelpUrlBuilder ..............
    basic_url : {self.url}
    meta_url : {self.meta_url}
    ........................... HelpUrlBuilder ..............
    """

    def get_url_type(self):
        from evdspy.EVDSlocal.index_requests.user_requests import UrlSeries
        url_type = UrlSeries()
        self.url_type = url_type

    @property
    def domain(self) -> str:
        return self.url_type.domain

    def clean(self, index: str) -> str:
        if "bie_" in index:
            return index
        return index.replace('_', '.')

    @property
    def basic_url(self) -> str:
        """
        https://evds2.tcmb.gov.tr/service/evds/serieList/type=xml&code=TP.DK.USD.A
        https://evds2.tcmb.gov.tr/service/evds/serieList/type=csv&code=bie_yssk
        https://evds2.tcmb.gov.tr/service/evds/serieList/type=json&code=TP.GSYIH02.GY.CF
        :return:
        """
        return f"https://evds2.tcmb.gov.tr/service/evds/serieList/type=json&code={self.index}"

    @property
    def url(self) -> str:
        return self.basic_url
