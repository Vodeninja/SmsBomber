from typing import Optional, Dict, Any
import re
import aiohttp


class CSRFHandler:
    @staticmethod
    def extract_from_html(html: str) -> Optional[str]:
        patterns = [
            r'<meta\s+name=["\']csrf[-_]?token["\']\s+content=["\']([^"\']+)["\']',
            r'<meta\s+name=["\']_csrf["\']\s+content=["\']([^"\']+)["\']',
            r'<input[^>]*name=["\'][^"\']*csrf[^"\']*["\'][^>]*value=["\']([^"\']+)["\']',
            r'<input[^>]*value=["\']([^"\']+)["\'][^>]*name=["\'][^"\']*csrf[^"\']*["\']',
            r'csrf[-_]?token["\']?\s*[:=]\s*["\']([^"\']+)["\']',
            r'["\']csrf["\']?\s*[:=]\s*["\']([^"\']+)["\']',
            r'["\']_csrf["\']?\s*[:=]\s*["\']([^"\']+)["\']',
            r'csrfToken["\']?\s*[:=]\s*["\']([^"\']+)["\']',
            r'__RequestVerificationToken["\']?\s*[:=]\s*["\']([^"\']+)["\']',
            r'authenticity_token["\']?\s*[:=]\s*["\']([^"\']+)["\']',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, html, re.IGNORECASE)
            if match:
                token = match.group(1)
                if len(token) > 8:
                    return token
        
        return None
    
    @staticmethod
    def extract_from_json(json_data: Dict[str, Any]) -> Optional[str]:
        json_str = str(json_data)
        patterns = [
            r'["\']csrf[-_]?token["\']\s*:\s*["\']([^"\']+)["\']',
            r'["\']_csrf["\']\s*:\s*["\']([^"\']+)["\']',
            r'["\']csrf["\']\s*:\s*["\']([^"\']+)["\']',
            r'["\']csrfToken["\']\s*:\s*["\']([^"\']+)["\']',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, json_str, re.IGNORECASE)
            if match:
                token = match.group(1)
                if len(token) > 8:
                    return token
        
        for key, value in json_data.items():
            if 'csrf' in key.lower() and isinstance(value, str) and len(value) > 8:
                return value
        
        return None
    
    @staticmethod
    def extract_from_cookies(cookies: Dict[str, str]) -> Optional[str]:
        for field_name in ['csrf', '_csrf', 'csrf_token', 'csrf-token', 'sessid', '_uss-csrf', 'PHPSESSID']:
            if field_name in cookies:
                return cookies[field_name]
        return None
    
    @staticmethod
    def extract_from_headers(headers: Dict[str, str]) -> Optional[str]:
        for key, value in headers.items():
            if 'csrf' in key.lower() and isinstance(value, str) and len(value) > 8:
                return value
        return None
    
    @staticmethod
    async def fetch_token(session: aiohttp.ClientSession, url: str, proxy: Optional[str] = None) -> Optional[str]:
        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            }
            
            async with session.get(url, headers=headers, proxy=proxy) as response:
                if response.status != 200:
                    return None
                
                content_type = response.headers.get('Content-Type', '').lower()
                
                if 'application/json' in content_type:
                    json_data = await response.json()
                    token = CSRFHandler.extract_from_json(json_data)
                else:
                    html = await response.text()
                    token = CSRFHandler.extract_from_html(html)
                
                if not token:
                    cookies = {name: cookie.value for name, cookie in response.cookies.items()}
                    token = CSRFHandler.extract_from_cookies(cookies)
                
                if not token:
                    headers_dict = dict(response.headers)
                    token = CSRFHandler.extract_from_headers(headers_dict)
                
                return token
        except Exception:
            return None
    
    @staticmethod
    def inject_into_data(data: Dict[str, Any], token: str) -> Dict[str, Any]:
        data = data.copy()
        for key, value in data.items():
            if 'csrf' in key.lower() and (value == "" or value is None):
                data[key] = token
                break
        return data
    
    @staticmethod
    def inject_into_headers(headers: Dict[str, Any], token: str) -> Dict[str, Any]:
        headers = headers.copy() if headers else {}
        
        for key, value in headers.items():
            if 'csrf' in key.lower() and (value == "" or value is None):
                headers[key] = token
                break
        
        if 'Cookie' in headers:
            cookie = headers['Cookie']
            csrf_pattern = r'(["\']?)(csrf|_csrf|csrf_token|csrf-token|sessid|_uss-csrf)\1\s*=\s*([^;]*?)(;|$)'
            matches = list(re.finditer(csrf_pattern, cookie, re.IGNORECASE))
            if matches:
                for match in matches:
                    field_name = match.group(2)
                    value_part = match.group(3)
                    if not value_part or value_part.strip() == '':
                        cookie = cookie[:match.start()] + f'{field_name}={token}' + cookie[match.end():]
                        headers['Cookie'] = cookie
                        break
        
        return headers
    
    @staticmethod
    def needs_csrf(kwargs: Dict[str, Any]) -> bool:
        if 'json' in kwargs:
            json_data = kwargs['json']
            if isinstance(json_data, dict):
                for key, value in json_data.items():
                    if 'csrf' in key.lower() and (value == "" or value is None):
                        return True
        
        if 'data' in kwargs and isinstance(kwargs['data'], dict):
            data = kwargs['data']
            for key, value in data.items():
                if 'csrf' in key.lower() and (value == "" or value is None):
                    return True
        
        headers = kwargs.get('headers', {})
        for key, value in headers.items():
            if 'csrf' in key.lower() and (value == "" or value is None):
                return True
        
        if 'Cookie' in headers:
            cookie = headers['Cookie']
            if re.search(r'(csrf|_csrf|csrf_token|csrf-token|sessid|_uss-csrf)\s*=\s*(;|$)', cookie, re.IGNORECASE):
                return True
        
        return False

