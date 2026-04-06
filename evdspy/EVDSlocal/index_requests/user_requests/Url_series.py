# ....................................................................... UrlSeries
class UrlSeries:
    @property
    def domain(self) -> str:
        return "https://evds3.tcmb.gov.tr/igmevdsms-dis/"

    @property
    def alias(self):
        return "series="




# ....................................................................... UrlDataGroup
class UrlDataGroup(UrlSeries):
    @property
    def alias(self):
        return "datagroup="
