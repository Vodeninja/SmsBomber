from abc import ABC, abstractmethod
from typing import Optional, Dict, Any
import aiohttp


class BaseService(ABC):
    def __init__(self, phone: str, proxy: Optional[str] = None):
        self.phone = phone
        self.proxy = proxy
        self.session: Optional[aiohttp.ClientSession] = None
    
    async def __aenter__(self):
        connector = aiohttp.TCPConnector(limit=100)
        timeout = aiohttp.ClientTimeout(total=30)
        
        if self.proxy:
            self.session = aiohttp.ClientSession(
                connector=connector,
                timeout=timeout,
                trust_env=True
            )
        else:
            self.session = aiohttp.ClientSession(
                connector=connector,
                timeout=timeout
            )
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
    
    @property
    @abstractmethod
    def name(self) -> str:
        pass
    
    @property
    @abstractmethod
    def url(self) -> str:
        pass
    
    @abstractmethod
    async def send_sms(self) -> Dict[str, Any]:
        pass
    
    async def _make_request(
        self,
        method: str,
        url: str,
        **kwargs
    ) -> aiohttp.ClientResponse:
        if not self.session:
            raise RuntimeError("Session not initialized")
        
        if self.proxy:
            kwargs['proxy'] = self.proxy
        
        async with self.session.request(method, url, **kwargs) as response:
            return response
    
    def _format_phone(self, phone: str) -> str:
        phone = phone.replace('+', '').replace(' ', '').replace('-', '').replace('(', '').replace(')', '')
        if phone.startswith('8') and len(phone) == 11:
            phone = '7' + phone[1:]
        return phone

