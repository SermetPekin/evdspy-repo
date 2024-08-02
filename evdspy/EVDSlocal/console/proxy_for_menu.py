import os


def get_proxies_env() -> dict:
    from ..config.dotenv import load_env
    def get_one(x, y):
        if x is None:
            return y
        return x

    load_env()  # http_proxy
    a = os.getenv("http_proxy")
    a1 = os.getenv("PROXY_http")

    b = os.getenv("https_proxy")
    b1 = os.getenv("PROXY_https")
    a = get_one(a, a1)
    b = get_one(b, b1)

    if a is None and b is None:
        return False
    if a and not b:
        return {"http": a}
    if b and not a:
        return {"https": b}
    return {
        "http": a,
        "https": b
    }

# check_proxy()
