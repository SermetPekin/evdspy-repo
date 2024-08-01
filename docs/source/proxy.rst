Proxy Configuration
===================

You can configure proxies for your application by defining them in a `.env` file. The script will load your proxies from this file if it is available.

Creating a `.env` File
----------------------

Create a `.env` file in the root directory of your project and define your proxies as shown below:

```bash
# Example .env file content
EVDS_API_KEY=AxByCzDsFoGmHeIgJaKrLbMaNgOe
PROXY_http=http://proxy.example.com:80
PROXY_https=http://proxy.example.com:80
```