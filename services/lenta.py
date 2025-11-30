from typing import Dict, Any
from core.base_service import BaseService
from utils import PhoneFormatter


class Lenta(BaseService):
    @property
    def name(self) -> str:
        return "lenta.com"

    @property
    def url(self) -> str:
        return "https://online.lenta.com/api.php"

    async def send_sms(self) -> Dict[str, Any]:
        formatted_phone = PhoneFormatter.format_with_brackets(self.phone)
        
        data = {
            "tel": formatted_phone
        }

        try:
            response = await self._make_request("POST", self.url, data=data)
            if response.status in [200, 201, 204]:
                return {"success": True, "message": "SMS sent successfully"}
            else:
                return {"success": False, "message": f"Status: {response.status}"}
        except Exception as e:
            return {"success": False, "message": str(e)}

