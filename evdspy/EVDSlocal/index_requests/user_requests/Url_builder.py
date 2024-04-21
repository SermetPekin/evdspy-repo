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

