import os


def get_proxies_env() -> dict:
    from ..config.dotenv import load_env
    load_env()
    a = os.getenv("PROXY_http")
    b = os.getenv("PROXY_https")

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
