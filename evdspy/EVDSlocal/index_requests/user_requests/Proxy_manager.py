# ....................................................................... ProxyManager
from dataclasses import dataclass
from typing import Optional, Any
from evdspy.EVDSlocal.console.proxy_for_menu import get_proxies_env


@dataclass
class ProxyManager:
    proxy: Optional[str] = None
    proxies: Optional[dict[Any, Any]] = None

    def get_proxies(self) -> Optional[dict[Any, Any]]:
        env_proxy = get_proxies_env()
        if self.proxies is None:
            if self.proxy is None:
                if env_proxy:
                    proxies = env_proxy
                else:
                    proxies = None
            else:
                proxies = self.get_proxies_helper()
        else:
            proxies = self.proxies
        # print("proxies", proxies)
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
