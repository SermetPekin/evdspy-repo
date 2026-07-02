# ....................................................................... ProxyManager
from dataclasses import dataclass
from typing import Optional, Any
from evdspy.EVDSlocal.console.proxy_for_menu import get_proxies_env


@dataclass
class ProxyManager:
    proxy: Optional[str] = None
    proxies: Optional[dict[Any, Any]] = None
    no_proxy : bool = False 
    
    def get_proxies(self) -> Optional[dict[Any, Any]]:
        if set_without_proxy() or self.no_proxy :  
            return None 
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
        return proxies

    def get_proxies_helper(self) -> Optional[dict[Any, Any]]:
        if self.proxy is None or self.no_proxy :
            return None
        proxy = self.proxy
        proxies = {
            'http': proxy,
            'https': proxy,
        }
        return proxies



import os
from typing import List, Union

def is_no_proxy_configured(domains: Union[str, List[str]]) -> bool:
    
    if isinstance(domains, str):
        domains = [domains]

    no_proxy = os.environ.get("no_proxy", "").lower()
    if not no_proxy:
        return False

    no_proxy_domains = [d.strip().lower() for d in no_proxy.split(",") if d.strip()]

    for domain in domains:
        domain = domain.strip().lower()
        if not domain:
            continue

        if domain in no_proxy_domains:
            return True

        if domain.startswith("*"):
            wildcard_suffix = domain[1:]   
            for no_proxy_domain in no_proxy_domains:
                if no_proxy_domain.endswith(wildcard_suffix):
                    return True

    return False

def set_without_proxy():
    import os 
    domains_to_check = ["evds3.tcmb.gov.tr", "*.tcmb.gov.tr" ] 
    return is_no_proxy_configured(domains_to_check)
