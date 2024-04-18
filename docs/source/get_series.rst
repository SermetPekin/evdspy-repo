
get_series Function
===================
The ``get_series`` function is designed to fetch economic data series from a specified API and return it formatted as a pandas DataFrame, making extensive use of various parameters to fine-tune the data retrieval process.
.. autofunction:: evdspy.get_series
Parameters
----------
index : str or tuple
    Identifier(s) for the data series to fetch. This can be a single string for one series or a tuple of strings for multiple series.
start_date : str, optional
    The start date for the data retrieval in 'DD-MM-YYYY' format. By default, this calls ``default_start_date_fnc()``.
end_date : str, optional
    The end date for the data retrieval in 'DD-MM-YYYY' format. By default, this calls ``default_end_date_fnc()``.
frequency : str, optional
    The frequency at which data should be retrieved, options include 'monthly', 'weekly', 'annually', 'semimonthly', 'semiannually', and 'business'.
formulas : str or tuple, optional
    Computation methods to apply to the data series, such as 'level', 'percentage_change', 'difference', 'year_to_year_percent_change', or 'year_to_year_differences'.
aggregation : str or tuple, optional
    Aggregation methods to apply to the data, options include 'avg', 'min', 'max', 'first', 'last', and 'sum'.
cache : bool, optional
    If True, uses cached data when available to speed up the data retrieval process. Default is False.
proxy : str, optional
    The URL of the proxy server to use for the requests. Default is None.
proxies : dict, optional
    A dictionary of proxies to use for the request. Default is None.
debug : bool, optional
    If True, runs the function in debug mode, providing additional debug information without making a real API request. Default is False.
api_key : str, optional
    The API key required for accessing the data. Initially, it can be saved using the ``save("APIKEY")`` function or via command line with ``$ evdspy save``.
Returns
-------
pd.DataFrame
    A pandas DataFrame containing the retrieved data series.
Raises
------
ValueError
    Raised if an invalid API key is provided or required parameters are missing.
Examples
--------
Basic usage:
.. code-block:: python
    index = "TP.ODEMGZS.BDTTOPLAM"
    df = get_series(index, start_date="01-01-2020", end_date="01-01-2021", frequency="monthly")
    print(df.head())
Using multiple indexes and cache:
.. code-block:: python
    indexes = ("TP.ODEMGZS.BDTTOPLAM", "TP.ODEMGZS.ABD")
    df = get_series(indexes, start_date="01-01-2020", frequency="monthly", cache=True)
    print(df.head())
.. code-block:: python
    template = """
    TP.ODEMGZS.BDTTOPLAM
    TP.ODEMGZS.ABD
    """
    df = get_series(template, start_date="01-01-2020", frequency="monthly", cache=True)
    print(df.head())
Applying formulas and aggregation:
.. code-block:: python
    df = get_series(template, start_date="01-01-2020", formulas="level", aggregation="sum")
    print(df.head())