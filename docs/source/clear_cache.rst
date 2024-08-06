
clear_cache Function
=======================

The ``clear_cache`` function deletes cache files that were saved inside .caches/evdspy folder 

.. code-block:: bash

    from evdspy import clear_cache 
    clear_cache()

If cache parameter is True this function will save time by using previously saved content in caches folder. 
default cache period is daily. It will only used if the previous successful request was made the current day.

.. code-block:: python


    index = """
    TP.DK.USD.A
    TP.DK.EUR.A
    TP.DK.CHF.A
    TP.DK.GBP.A
    TP.DK.JPY.A


    """
    df = get_series(index, cache=True ,  start_date="01-01-2017", end_date="31-12-2017" )
    print(df.head())