Introduction
===============================

.. image:: https://github.com/SermetPekin/evdspy-repo/actions/workflows/python-package.yml/badge.svg
    :target: https://github.com/SermetPekin/evdspy-repo/actions/workflows/python-package.yml
.. image:: https://img.shields.io/pypi/v/evdspy
    :target: https://pypi.org/project/evdspy/
.. image:: https://img.shields.io/pypi/pyversions/evdspy
    :target: https://pypi.org/project/evdspy/
.. image:: https://pepy.tech/badge/evdspy/week
    :target: https://pepy.tech/project/evdspy

evdspy is an open-source Python interface that simplifies making requests to the Central Bank of the Republic of Turkey (CBRT) Electronic Data Delivery System (EVDS). It provides efficient request handling by caching results, a user-friendly menu for data inquiries, and capabilities for handling complex data structures through an accessible API.

View Source Code
----------------
You can view the source code for this project on GitHub: `View Source <https://github.com/SermetPekin/evdspy-repo>`_.

What's New
----------

Updated in this version:
------
- The API key parameter has been moved to the HTTP header to enhance security and ensure that sensitive information is not exposed in URLs.
- Added a new function, ``get_series``, which improves the handling of data groups and series.
- Deprecated: The ``get_datagroup`` function will be deprecated in future versions; ``get_series`` will cover its functionalities.

- evdspyChat Application Added

  The evdspyChat application has been added. An API key is not required for questions related to evdspy documentation.


`evdspyChat <https://evdspychat.onrender.com/>`_


.. image:: https://github.com/user-attachments/assets/14024132-4d41-4879-9ea8-3e510b2f8f02
    :target: https://evdspychat.onrender.com/






.. image:: https://github.com/user-attachments/assets/14024132-4d41-4879-9ea8-3e510b2f8f02
    :target: https://evdspychat.onrender.com/



.. image:: https://github.com/user-attachments/assets/2cece3e0-958a-454b-8876-5dbdfea1e1a4
    :target: https://evdspychat.onrender.com/

.. image:: https://github.com/user-attachments/assets/3e5d3ab4-df41-4d34-8e2a-e1ca3d19a190
    :target: https://evdspychat.onrender.com/


.. image:: https://github.com/user-attachments/assets/3e5d3ab4-df41-4d34-8e2a-e1ca3d19a190
    :target: https://evdspychat.onrender.com/




Key Features
------------
- **API Key Management**: Automatically saves the API key to a file when provided to the ``get_series`` function, ignoring subsequent entries unless explicitly updated.
- **Visual and Textual Menu Options**: Provides both visual and textual menus to facilitate user interaction for setting up projects, creating output folders, and preparing configuration files.
- **Data Request Handling**: Utilizes caching to optimize data retrieval, minimizing redundant requests and speeding up the data access process.

Installation
------------
To install evdspy, simply run the following command:

.. code-block:: bash

    pip install evdspy -U

Quick Start
-----------
Here's a quick example to get you started with using evdspy:

using get_series function from evdspy 

.. code-block:: python
    
    from evdsy import get_series 
    index = "TP.ODEMGZS.BDTTOPLAM"
    df = get_series(index, start_date="21-01-2020", end_date="31-12-2021", frequency="monthly")
    print(df.head())


using get_series_exp function from evdspy 

.. code-block:: python

    from evdsy import get_series , get_series_exp
    index = "TP.ODEMGZS.BDTTOPLAM"
    result   = get_series_exp(index, start_date="21-01-2020", end_date="31-12-2021", frequency="monthly")
    print(result.data )               # data frame of data 
    print(result.metadata )           # metadata frame of data 
    result.to_excel('filename.xlsx')  # write output as excel file data and metadata in sheets 





