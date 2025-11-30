from typing import List, Optional
import random


class ProxyManager:
    def __init__(self, proxies: Optional[List[str]] = None):
        self.proxies = proxies or []
        self.current_index = 0
    
    def add_proxy(self, proxy: str):
        if proxy and proxy not in self.proxies:
            self.proxies.append(proxy)
    
    def load_from_file(self, filepath: str):
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                proxies = [line.strip() for line in f if line.strip()]
                self.proxies.extend(proxies)
        except FileNotFoundError:
            pass
    
    def get_random(self) -> Optional[str]:
        if not self.proxies:
            return None
        return random.choice(self.proxies)
    
    def get_round_robin(self) -> Optional[str]:
        if not self.proxies:
            return None
        proxy = self.proxies[self.current_index]
        self.current_index = (self.current_index + 1) % len(self.proxies)
        return proxy
    
    def get_all(self) -> List[str]:
        return self.proxies.copy()
    
    def has_proxies(self) -> bool:
        return len(self.proxies) > 0

