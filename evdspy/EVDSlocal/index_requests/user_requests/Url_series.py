# ....................................................................... UrlSeries
class UrlSeries:
    @property
    def domain(self) -> str:
        return "https://evds2.tcmb.gov.tr/service/evds"

    @property
    def alias(self):
        return "series="



# ....................................................................... UrlDataGroup
class UrlDataGroup(UrlSeries):
    @property
    def alias(self):
        return "datagroup="
