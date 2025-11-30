from typing import Dict, Any
from core.base_service import BaseService
from utils import PhoneFormatter


class Hungrygator(BaseService):
    @property
    def name(self) -> str:
        return "hungrygator.ru"

    @property
    def url(self) -> str:
        return "https://api.01.hungrygator.ru/web/auth/webotp"

    async def send_sms(self) -> Dict[str, Any]:
        formatted_phone = PhoneFormatter.format_with_brackets(self.phone)
        
        data = {
            "userLogin": formatted_phone,
            "fu": "bar"
        }
        headers = {
            "Content-Type": "application/json"
        }

        try:
            response = await self._make_request("POST", self.url, json=data, headers=headers)
            if response.status in [200, 201, 204]:
                return {"success": True, "message": "SMS sent successfully"}
            else:
                return {"success": False, "message": f"Status: {response.status}"}
        except Exception as e:
            return {"success": False, "message": str(e)}

