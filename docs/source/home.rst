
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

evdspy is an open-source Python interface that simplifies making requests to the Central Bank of the Republic of Turkey (CBRT) Economic Data Service (EDS). It provides efficient request handling by caching results, a user-friendly menu for data inquiries, and capabilities for handling complex data structures through an accessible API.

View Source Code
----------------
You can view the source code for this project on GitHub: `View Source <https://github.com/SermetPekin/evdspy-repo>`_.

What's New
----------
**Updated on this version:**
- The API key parameter has now been moved to the HTTP header to enhance security and ensure that sensitive information is not exposed in URLs.
- Added a new function, ``get_series``, which enhances the way data groups and series are handled.
- Deprecated: The ``get_datagroup`` function will be deprecated in future versions; ``get_series`` will cover its functionalities.

### Updated on this version

#### evdspyChat application was added. 

Api Key is not required for only evdspy documentation related questions.

[evdspyChat](https://evdspychat-b11f96868cb6.herokuapp.com/)

   [![tellme](https://github.com/user-attachments/assets/14024132-4d41-4879-9ea8-3e510b2f8f02)](https://evdspychat-b11f96868cb6.herokuapp.com/)
   
[![askyourself](https://github.com/user-attachments/assets/2cece3e0-958a-454b-8876-5dbdfea1e1a4)](https://evdspychat-b11f96868cb6.herokuapp.com/)

[![a2](https://github.com/user-attachments/assets/3e5d3ab4-df41-4d34-8e2a-e1ca3d19a190)](https://evdspychat-b11f96868cb6.herokuapp.com/)


Key Features
------------
- **API Key Management**: Automatically saves the API key to a file when provided to the ``get_series`` function, ignoring subsequent entries unless explicitly updated.
- **Visual and Textual Menu Options**: Provides both a visual and textual menu to facilitate user interaction for setting up projects, creating output folders, and preparing configuration files.
- **Data Request Handling**: Utilizes caching to optimize data retrieval, minimizing redundant requests and speeding up the data access process.

Installation
------------
To install evdspy, simply run the following command:
.. code-block:: bash

    pip install evdspy -U

Quick Start
-----------
Here's a quick example to get you started with using evdspy:

.. code-block:: python

    from evdspy import get_series, default_start_date_fnc, default_end_date_fnc
    index = "TP.ODEMGZS.BDTTOPLAM", "TP.ODEMGZS.ABD"
    df = get_series(index, frequency="monthly", start_date=default_start_date_fnc(), end_date=default_end_date_fnc(), aggregation=("avg",), cache=True)
    print(df)

API Usage Examples
------------------

.. literalinclude:: ../../evdspy_example.py
   :language: python
   :linenos:
   :caption: Example of using the get_series function to retrieve data.

Menus and Commands
------------------
- **Main Menu**: Access a user-friendly menu to manage data requests and settings.
- **Console Commands**: Use terminal commands to manage settings and request data:

  .. code-block:: bash

      evdspy setup
      evdspy menu
      evdspy create series
      evdspy help
      evdspy get

Learn More
----------
For more detailed information on all functions and their parameters, refer to the *Modules* section or visit our [GitHub Repository](https://github.com/SermetPekin/evdspy-repo).

Disclaimer
----------
Please note that evdspy is not officially affiliated with or endorsed by the CBRT. It is developed and maintained under an MIT license by independent developers. Use of this tool should comply with all applicable laws and API usage guidelines provided by the CBRT.

