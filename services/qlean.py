from typing import Dict, Any
from core.base_service import BaseService


class Qlean(BaseService):
    @property
    def name(self) -> str:
        return "qlean.ru"

    @property
    def url(self) -> str:
        return "https://qlean.ru/widget-form/http/requestotp"

    async def send_sms(self) -> Dict[str, Any]:
        phone = self._format_phone(self.phone)
        
        data = {
            "connection": 3,
            "csrfToken": "1a55c5d16d8059e75304cb02ddda566b7d2a96bd22cc92937ee5a894e6dfa734",
            "login": phone,
            "send": 1,
            "userAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.53 Safari/537.36 Edg/103.0.1264.37",
            "userType": 1
        }
        headers = {
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.53 Safari/537.36 Edg/103.0.1264.37"
        }

        try:
            response = await self._make_request("POST", self.url, json=data, headers=headers)
            if response.status in [200, 201, 204]:
                return {"success": True, "message": "SMS sent successfully"}
            else:
                return {"success": False, "message": f"Status: {response.status}"}
        except Exception as e:
            return {"success": False, "message": str(e)}

