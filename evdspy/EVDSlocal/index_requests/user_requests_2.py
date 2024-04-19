"""
class UrlSeries:
    @property
    def domain(self) -> str:
        return "https://evds2.tcmb.gov.tr/service/evds"
    @property
    def alias(self):
        return "series="



"""
from evdspy.EVDSlocal.index_requests.user_requests import UrlSeries, UrlBuilder


class CategoriesMetadata(UrlSeries):
    def get_url(self):
        return f"{self.domain}/categories/type=json"

    @property
    def url(self):
        return self.get_url()


class DataGroup_info():
    def __init__(self, table_name):
        self.table_name = table_name


class DatagroupsMetadata(UrlSeries):
    def __init__(self, data_group: DataGroup_info):
        self.data_group = data_group

    def get_url(self):
        # "https://evds2.tcmb.gov.tr/service/evds/datagroups/mode=1&code=bie_yssk&type=json"
        # self.table_name = self.table_name  # "bie_yssk"
        return f"{self.domain}/datagroups/mode=1&code={self.data_group.table_name}&type=json"

    @property
    def url(self):
        return self.get_url()


def test_CategoriesMetadata(capsys):
    with capsys.disabled():
        d = DataGroup_info("bie_yssk")
        assert d.table_name == "bie_yssk"
        a = DatagroupsMetadata(d)
        print(a.url)
        b = CategoriesMetadata()
        print(b.url)


class UrlBuilderMetadata(UrlBuilder):
    ...

    def get_url(self):
        ...

    def categories(self):
        """"""
        # 4.1 Category Service
        # https://evds2.tcmb.gov.tr/service/evds/categories/type=json

    def datagroups_mode_1(self, name="bie_yssk"):
        """
        https://evds2.tcmb.gov.tr/service/evds/datagroups/mode=1&code=bie_yssk&type=json
        :return:
        """
        ...

    def datagroups_mode_2(self, code=1):
        """
        https://evds2.tcmb.gov.tr/service/evds/datagroups/mode=2&code=2&type=json
        :return:
        """
        ...

    def data_group_service(self):
        """data_group_service"""
        """
        The data group listing is based on the following filtering:
            mode=0 Returns all data groups under all categories.
            mode=1 Returns data group information according to a data group selection.
            mode=2 Returns all data groups information according to a category
            mode 1
                code=data group code
            mode 2
                code=category code
            https://evds2.tcmb.gov.tr/service/evds/datagroups/mode=1&code=bie_yssk&type=json
            https://evds2.tcmb.gov.tr/service/evds/datagroups/mode=2&code=2&type=xml
            DATAGROUP_CODE Data Group Code
            DATAGROUP_NAME Data Group Name (Turkish)
            DATAGROUP_NAME_ENG Data Group Name (English)
            START_DATE Data Start Date
            END_DATE Date End Date
            FREQUENCY Original Frequency
            FREQUENCY_STR Original Frequency Desc.
            DATASOURCE Data Source (Turkish)
            DATASOURCE_ENG Data Source (English)
            METADATA_LINK Metadata Link (Turkish)
            METADATA_LINK_ENG Metadata Link (English)
            REV_POL_LINK Revision Policy Link (Turkish)
            REV_POL_LINK_ENG Revision Policy Link (English)
            APP_CHA_LINK Application Change Link (Turkish)
            APP_CHA_LINK_ENG Application Change Link (English)
            NOTE Information Note (Turkish)
            NOTE_ENG Information Note (English)
        """
        # 4.2 Data Group Service


from abc import ABC, abstractmethod


class GuideMetadata:
    def get_meta(self):
        ...

    def display_meta(self):
        ...


class UrlBuilderMetadataCategories(UrlBuilderMetadata, GuideMetadata):
    """
    UrlBuilderMetadataCategories
    """


class UrlBuilderMetadataDataGroup(UrlBuilderMetadata, GuideMetadata):
    """
    UrlBuilderMetadataCategories
    """
