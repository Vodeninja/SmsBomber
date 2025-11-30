from typing import Dict, Any
from core.base_service import BaseService


class Telegram(BaseService):
    @property
    def name(self) -> str:
        return "telegram.org"

    @property
    def url(self) -> str:
        return "https://my.telegram.org/auth/send_password"

    async def send_sms(self) -> Dict[str, Any]:
        phone = self._format_phone(self.phone)
        
        data = {
            "phone": f"+{phone}"
        }

        try:
            response = await self._make_request("POST", self.url, data=data)
            if response.status in [200, 201, 204]:
                return {"success": True, "message": "SMS sent successfully"}
            else:
                return {"success": False, "message": f"Status: {response.status}"}
        except Exception as e:
            return {"success": False, "message": str(e)}

