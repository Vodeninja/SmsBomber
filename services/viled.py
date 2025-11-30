from typing import Dict, Any
from core.base_service import BaseService


class Viled(BaseService):
    @property
    def name(self) -> str:
        return "viled.kz"

    @property
    def url(self) -> str:
        return "https://api-prod.viled.kz/tizilimer/api/v1/users/sms"

    async def send_sms(self) -> Dict[str, Any]:
        phone = self._format_phone(self.phone)
        
        params = {
            "phone": phone
        }
        headers = {
            "accept": "*/*",
            "accept-language": "ru",
            "content-type": "application/json; charset=UTF-8",
            "currency": "KZT",
            "locale": "ru",
            "origin": "https://viled.kz",
            "referer": "https://viled.kz/",
            "sec-ch-ua": '"Microsoft Edge";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 Edg/123.0.0.0"
        }

        try:
            response = await self._make_request("GET", self.url, params=params, headers=headers)
            if response.status in [200, 201, 204]:
                return {"success": True, "message": "SMS sent successfully"}
            else:
                return {"success": False, "message": f"Status: {response.status}"}
        except Exception as e:
            return {"success": False, "message": str(e)}

