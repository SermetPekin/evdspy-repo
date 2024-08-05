Examples 
====================

Some examples to retrieve data 


Basic usage:

.. code-block:: python

    .. https://evds2.tcmb.gov.tr/service/evds/series=
    .. TP.DK.USD.A-TP.DK.EUR.A-TP.DK.CHF.A-TP.DK.GBP.A-TP.DK.JPY.A&startDate=01-10-2017&endDate=01-11-2017&type=xml


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

    indexes = ("TP.ODEMGZS.BDTTOPLAM", "TP.ODEMGZS.ABD")
    df = get_series(indexes, start_date="01-01-2020", frequency="monthly", cache=True)
    print(df.head())

Applying formulas and aggregation:

.. code-block:: python

    template = "TP.ODEMGZS.BDTTOPLAM"
    df = get_series(template, start_date="01-01-2020", formulas="level", aggregation="sum")
    print(df.head())