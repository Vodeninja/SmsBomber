from abc import ABC, abstractmethod
from typing import Optional, Dict, Any
import aiohttp
from utils import CSRFHandler, PhoneFormatter, CSRFGenerator


class BaseService(ABC):
    def __init__(self, phone: str, proxy: Optional[str] = None):
        self.phone = phone
        self.proxy = proxy
        self.session: Optional[aiohttp.ClientSession] = None
        self._csrf_token: Optional[str] = None
        self._csrf_url: Optional[str] = None
    
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
    
    def get_csrf_url(self) -> Optional[str]:
        return self._csrf_url
    
    @abstractmethod
    async def send_sms(self) -> Dict[str, Any]:
        pass
    
    def _format_phone(self, phone: str) -> str:
        return PhoneFormatter.format(phone)
    
    async def _fetch_csrf_token(self) -> Optional[str]:
        if self._csrf_token is not None:
            return self._csrf_token
        
        csrf_url = self.get_csrf_url() or self.url
        self._csrf_token = await CSRFHandler.fetch_token(self.session, csrf_url, self.proxy)
        return self._csrf_token
    
    async def _get_csrf_token(self) -> str:
        if self._csrf_token is None:
            await self._fetch_csrf_token()
        
        if self._csrf_token is None:
            self._csrf_token = CSRFGenerator.generate_hex(32)
        
        return self._csrf_token
    
    async def _make_request(
        self,
        method: str,
        url: str,
        **kwargs
    ) -> aiohttp.ClientResponse:
        if not self.session:
            raise RuntimeError("Session not initialized")
        
        if CSRFHandler.needs_csrf(kwargs):
            await self._fetch_csrf_token()
            csrf_token = await self._get_csrf_token()
            
            if 'json' in kwargs and isinstance(kwargs['json'], dict):
                kwargs['json'] = CSRFHandler.inject_into_data(kwargs['json'], csrf_token)
            elif 'data' in kwargs and isinstance(kwargs['data'], dict):
                kwargs['data'] = CSRFHandler.inject_into_data(kwargs['data'], csrf_token)
            
            if 'headers' in kwargs:
                kwargs['headers'] = CSRFHandler.inject_into_headers(kwargs['headers'], csrf_token)
            else:
                kwargs['headers'] = CSRFHandler.inject_into_headers({}, csrf_token)
        
        if self.proxy:
            kwargs['proxy'] = self.proxy
        
        async with self.session.request(method, url, **kwargs) as response:
            return response

