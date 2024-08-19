Examples 
====================

Some examples to retrieve data 


Basic usage:

.. code-block:: python


    index = """
    TP.DK.USD.A
    TP.DK.EUR.A
    TP.DK.CHF.A
    TP.DK.GBP.A
    TP.DK.JPY.A


    """
    df = get_series(index, start_date="01-01-2017", end_date="31-12-2017" )
    print(df.head())



Using multiple indexes and cache:

.. code-block:: python

    from evdspy import get_series , get_series_exp 
    index = """
    TP.DK.USD.A
    TP.DK.EUR.A
    TP.DK.CHF.A
    TP.DK.GBP.A
    TP.DK.JPY.A


    """
    result = get_series_exp(index, start_date="01-01-2017", end_date="31-12-2017" )
    print(result.data)
    print(result.metadata)

cache True for eficient requests. Only checks request result for the current day. 

.. code-block:: python

    from evdspy import get_series , get_series_exp 
    index = """
    TP.DK.USD.A
    TP.DK.EUR.A
    TP.DK.CHF.A
    TP.DK.GBP.A
    TP.DK.JPY.A


    """
    result = get_series_exp(index, cache = True  , start_date="01-01-2017", end_date="31-12-2017" )
    print(result.data)



.. code-block:: python

    from evdspy import get_series , get_series_exp 



    CPI = """
    TP.FG.J0  # Consumer Price Index 
    """

    inf_exp_market_part = """

    TP.ENFBEK.PKA12ENF # Annual inflation expectations of market participants (12-month ahead, %) 

    """
    inf_exp_real_sector = """

    TP.ENFBEK.IYA12ENF # Annual inflation expectations of real sector (12-month ahead, %) 

    """


    for index  in [CPI, inf_exp_market_part, inf_exp_real_sector]:
        res = get_series_exp(index , cache = True  , start_date = "01-01-2010" )
        print(res.data)
        print(res.metadata)

