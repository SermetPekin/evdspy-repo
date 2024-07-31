from dataclasses import dataclass, field
from typing import Union, Any, Optional, Literal, Callable
import pandas as pd
from evdspy.EVDSlocal.index_requests.user_requests.Request_config import RequestConfig
from evdspy.EVDSlocal.index_requests.get_series_indexes_utils import (
    default_start_date_fnc,
    default_end_date_fnc,
)


def initial_api_process_when_given(api_key: Optional[str] = None) -> None:
    from evdspy.EVDSlocal.config.apikey_class import ApikeyClass

    if api_key is None:
        return
    if ApikeyClass().get_valid_api_key(check=False) is False:
        from evdspy.EVDSlocal.initial.load_commands_cmds_to_load import save_apikey

        save_apikey(api_key)


def create_metadata_url(series_code: str, response_type: str = 'json') -> str:
    base_url = "https://evds2.tcmb.gov.tr/service/evds/serieList"
    return f"{base_url}?type={response_type}&code={series_code}&mode=2"


def get_metadata_for_index(index: Union[str, tuple[Any, ...]], proxy_manager: Any, cache=True) -> pd.DataFrame:
    from evdspy.EVDSlocal.index_requests.user_requests import ApiRequester, DataProcessor
    from evdspy.EVDSlocal.index_requests.user_requests.Url_builder import HelpUrlBuilder

    config = RequestConfig(index, cache=False)  # TODO

    def get(index_local):
        config_local = RequestConfig(index_local, cache=cache)
        help_url_builder = HelpUrlBuilder(config_local)
        api_requester = ApiRequester(help_url_builder, proxy_manager)
        metadata_processor = DataProcessor(api_requester())
        return metadata_processor()

    metas = tuple(map(get, config.index))
    return pd.concat(metas, axis="rows", join="outer")


@dataclass
class Result:
    """
    get_series_exp function returns instance of this class
    data : pd.DataFrame
    metadata : pd.DataFrame
    write : creates and Excel file with data and metadadata of two sheets
    to_excel : same with write to meet pandas to_excel function
    """
    data: field(default_factory=pd.DataFrame)
    metadata: field(default_factory=pd.DataFrame)
    write: Callable

    def __post_init__(self):
        self.to_excel = self.write

    def __str__(self):
        content = super.__str__(self)

        return """
    ! get_series_exp function returns instance of this class 
    <Result>
    data     : pd.DataFrame  => contains data [ same as what get_series function returns ] 
    metadata : pd.DataFrame  => contains metadata if available 
    write    : Callable      => creates and Excel file with data and metadadata of two sheets 
    to_excel : Callable      =>  same with write to meet pandas to_excel function 
    
        """ + content


def get_series_exp(
        index: Union[str, tuple[Any, ...]],
        start_date: str = default_start_date_fnc(),
        end_date: str = default_end_date_fnc(),
        frequency: Union[
            Literal[
                "monthly", "weekly", "annually", "semimonthly", "semiannually", "business", None
            ]
        ] = None,
        formulas: Union[Literal["level", "percentage_change", "difference"], None] = None,
        aggregation: Union[
            Literal["avg", "min", "max", "first", "last", "sum", None], None
        ] = None,
        cache: bool = True,
        meta_cache: bool = True,
        proxy: Optional[str] = None,
        proxies: Optional[dict[str, str]] = None,
        debug: bool = False,
        api_key: Optional[str] = None,
) -> dict[str, pd.DataFrame]:
    """
    Retrieves economic data series from the specified API and returns it as a pandas DataFrame.
    Parameters
    ----------
    index : str or tuple of str
        The identifier(s) for the data series to fetch. Can be a single string for one series or a tuple of strings for multiple series.
    start_date : str, optional
        The start date for the data retrieval in 'DD-MM-YYYY' format, by default calls default_start_date_fnc().
    end_date : str, optional
        The end date for the data retrieval in 'DD-MM-YYYY' format, by default calls default_end_date_fnc().
    frequency : str, optional
        The frequency at which data should be retrieved.
        monthly | weekly | annually | semimonthly | semiannually | business
    formulas : str or tuple of str, optional
        The computation methods to apply to the data series
        level | percentage_change | difference | year_to_year_percent_change | year_to_year_differences
    aggregation : str or tuple of str, optional
        The aggregation methods to apply to the data, similar to formulas.
        avg |min | max | first | last | sum
    cache : bool, optional
        If True, uses cached data when available to speed up the data retrieval process, by default False.
    meta_cache : bool, optional
        If True, uses cached data for metadata when available to speed up the data retrieval process, by default False.
    proxy : str, optional
        The URL of the proxy server to use for the requests, by default None.
    proxies : dict, optional
        A dictionary of proxies to use for the request, by default None.
    debug : bool, optional
        If True, runs the function in debug mode, providing additional debug information without making a real API request, by default False.
    api_key : str, optional
        The API key required for accessing the data, by default None.
        When it was given for the first time it will be saved to a file for the subsequent requests.
        alternatively it may be saved by save("APIKEY") function or $ evdspy save [from console]
    Returns
    -------
    pd.DataFrame
        A pandas DataFrame containing the retrieved data series.
    Raises
    ------
    ValueError
        If an invalid API key is provided or required parameters are missing.
    """

    from evdspy.EVDSlocal.index_requests.user_requests import (
        RequestConfig,
        ProxyManager,
        UrlBuilder,
        DataProcessor,
    )
    from evdspy.EVDSlocal.index_requests.user_requests.Api_requester import ApiRequester

    # ............initial_api_process_when_given...............
    initial_api_process_when_given(api_key)
    # ............RequestConfig................................
    config = RequestConfig(
        index=index,
        start_date=start_date,
        end_date=end_date,
        frequency=frequency,
        formulas=formulas,
        aggregation=aggregation,
        cache=cache,
    )
    # ............ProxyManager................................
    proxy_manager = ProxyManager(proxy=proxy, proxies=proxies)
    # ............UrlBuilder..................................
    url_builder = UrlBuilder(config, url_type=None)
    # ............ApiRequester................................
    api_requester = ApiRequester(url_builder, proxy_manager)
    if debug:
        return api_requester.dry_request()
    # ............DataProcessor................................
    data_processor = DataProcessor(api_requester())

    # Fetch the main data
    main_data = data_processor()

    # Fetch metadata for each index
    metadata_: pd.DataFrame = get_metadata_for_index(index, proxy_manager, cache=meta_cache)
    # return pd.DataFrame(liste)

    result = {
        "main_data": main_data,
        "metadata": metadata_,
    }

    def build_df(file_name='output.xlsx'):
        res = False
        with pd.ExcelWriter(file_name) as writer:
            for sheet_name, df in result.items():
                if isinstance(df, pd.DataFrame):
                    df.to_excel(writer, sheet_name=sheet_name, index=False)
                    res = True
        if res:
            print(f" writing file :  [{file_name}] ")

    return Result(main_data, metadata_, build_df)


def test_get_series2(capsys):
    with capsys.disabled():
        # setup()
        result = get_series_exp("TP.ODEMGZS.BDTTOPLAM", cache=False)
        assert isinstance(result['main_data'], pd.DataFrame)
        assert isinstance(result['metadata'], pd.DataFrame)


__all__ = ("get_series_exp",)
