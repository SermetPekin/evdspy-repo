Api Key Configuration
==========================

You can configure api_key and proxies for your application by defining them in a `.env` file. The script will load your proxies from this file if it is available.

Creating a `.env` File
==========================

Create a `.env` file in the root directory of your project and define your proxies as shown below:


.. code-block:: bash 

    # Example .env file content
    EVDS_API_KEY=AxByCzDsFoGmHeIgJaKrLbMaNgOe


If you run your code behind proxy you may set your proxy addres in .env file 

.. code-block:: bash 

    # Example .env file content
    EVDS_API_KEY=AxByCzDsFoGmHeIgJaKrLbMaNgOe
    
    http_proxy=http://proxy.example.com:80
    https_proxy=http://proxy.example.com:80
    

Replace `http://proxy.example.com:80` with the actual URL and port of your proxy server.

Setting Environment Variables
=============

Windows
----------

To set environment variables on Windows, you can use the `setx` command in the Command Prompt:

.. code-block:: bash
  
    set EVDS_API_KEY=AxByCzDsFoGmHeIgJaKrLbMaNgOe
    set http_proxy=http://proxy.example.com:80  
    set https_proxy=http://proxy.example.com:80


Linux and macOS
------------------
To set environment variables on Linux or macOS, you can use the `export` command in the terminal:

.. code-block:: bash

    export EVDS_API_KEY="AxByCzDsFoGmHeIgJaKrLbMaNgOe"
    export http_proxy="http://proxy.example.com:80"
    export https_proxy="http://proxy.example.com:80"

You can add these lines to your shell configuration file (e.g., `.bashrc`, `.bash_profile`, `.zshrc`) to make them persistent.

Notes
----------

- Replace `http://proxy.example.com:80` with the actual URL and port of your proxy server.
- For the API key and proxy settings to take effect, you might need to restart your terminal or Command Prompt session.
