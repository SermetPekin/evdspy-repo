# ....................................................................... ProxyManager
from dataclasses import dataclass
from typing import Optional, Any


@dataclass
class ProxyManager:
    proxy: Optional[str] = None
    proxies: Optional[dict[Any, Any]] = None

    def get_proxies(self) -> Optional[dict[Any, Any]]:
        if self.proxies is None:
            if self.proxy is None:
                proxies = None
            else:
                proxies = self.get_proxies_helper()
        else:
            proxies = self.proxies
        return proxies

    def get_proxies_helper(self) -> Optional[dict[Any, Any]]:
        if self.proxy is None:
            return None
        proxy = self.proxy
        proxies = {
            'http': proxy,
            'https': proxy,
        }
        return proxies
