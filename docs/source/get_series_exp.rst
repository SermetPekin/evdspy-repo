get_series_exp Function
=======================

The ``get_series_exp`` function fetches economic data series from a specified API and returns it formatted as a pandas DataFrame. This function offers various parameters to fine-tune the data retrieval process.

.. autofunction:: evdspy.get_series_exp

Parameters
----------
index : str or tuple
    Identifier(s) for the data series to fetch. This can be a single string for one series or a tuple of strings for multiple series.

start_date : str, optional
    The start date for the data retrieval in 'DD-MM-YYYY' format. By default, this calls ``default_start_date_fnc()``.

end_date : str, optional
    The end date for the data retrieval in 'DD-MM-YYYY' format. By default, this calls ``default_end_date_fnc()``.

frequency : str, optional
    The frequency at which data should be retrieved. Options include:

    - **daily (1)**: Data retrieved every day.
    - **business (2)**: Data retrieved only on business days.
    - **weekly (3)**: Data retrieved weekly on Fridays.
    - **semimonthly (4)**: Data retrieved twice a month.
    - **monthly (5)**: Data retrieved once a month.
    - **quarterly (6)**: Data retrieved every quarter.
    - **semiannually (7)**: Data retrieved twice a year.
    - **annual/annually (8)**: Data retrieved once a year.

formulas : str or tuple, optional
    Computation methods to apply to the data series. Options include:

    - **level (0)**: Raw data values.
    - **percentage change (1)**: Percent change between consecutive data points.
    - **difference (2)**: Difference between consecutive data points.
    - **year to year percent change (3)**: Percent change from the same date in the previous year.
    - **year to year differences (4)**: Difference from the same date in the previous year.
    - **percentage change compared to end-of-previous year (5)**: Percent change relative to the end of the previous year.
    - **difference compared to end-of-previous year (6)**: Difference relative to the end of the previous year.
    - **moving average (7)**: Moving average of data points.
    - **moving sum (8)**: Moving sum of data points.

aggregation : str or tuple, optional
    Aggregation methods to apply to the data. Options include:

    - **avg**: Average value over the specified period.
    - **min**: Minimum value over the specified period.
    - **max**: Maximum value over the specified period.
    - **first**: First value within the specified period.
    - **last**: Last value within the specified period.
    - **sum**: Sum of all values within the specified period.

cache : bool, optional
    If True, uses cached data when available to speed up the data retrieval process. Default is False.

meta_cache : bool, optional
    If True, uses cached metadata when available to speed up the data retrieval process. Default is False.

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
Result Class
    An object containing the following attributes:

    data : pd.DataFrame
        The retrieved data series.

    metadata : pd.DataFrame
        Metadata associated with the data series, if available.

    write : Callable
        Function to create an Excel file with data and metadata in two sheets.

    to_excel : Callable
        Same as `write`, for compatibility with pandas' `to_excel` function.

Raises
------
ValueError
    Raised if an invalid API key is provided or required parameters are missing.


Creating a `.env` File
=============

Create a `.env` file in the root directory of your project and define your proxies as shown below:


.. code-block:: bash 

    # Example .env file content
    EVDS_API_KEY=AxByCzDsFoGmHeIgJaKrLbMaNgOe
    
Examples
--------
Basic usage:

.. code-block:: python

    from evdspy import get_series_exp

    template = """

    TP.KREDI.L002
    TP.BFTUKKRE.L004 
    TP.BFTUKKRE.L056
    TP.BFTUKKRE.L193 
    TP.BFTUKKRE.L234 
    """

    result = get_series_exp(index, start_date="01-01-2020", end_date="01-01-2021", frequency="monthly")
    print(result.data.head())
    print(result.metadata)
    result.write('output1.xlsx')
    result.to_excel('output2.xlsx')

Using multiple indexes and cache:

.. code-block:: python
    
    from evdspy import get_series_exp

    indexes = ("TP.ENFBEK.PKA12ENF", "TP.ENFBEK.IYA12ENF")
    result = get_series_exp(indexes, start_date="01-01-2020", end_date="01-01-2021", frequency="monthly")
    print(result.data.head())
    print(result.metadata)
    result.write('output1.xlsx')
    result.to_excel('output2.xlsx')

Applying formulas and aggregation:

.. code-block:: python

    from evdspy import get_series_exp

    template = """
    
    TP.KREDI.L002
    TP.BFTUKKRE.L004 
    TP.BFTUKKRE.L056
    TP.BFTUKKRE.L193 
    TP.BFTUKKRE.L234 
    """

    result = get_series_exp(template, formulas="level", aggregation="sum")
    print(result.data.head())
    print(result.metadata)
    result.write('output.xlsx')
    result.to_excel('output2.xlsx')
