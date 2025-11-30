from typing import Dict, Any
from core.base_service import BaseService
from utils import PhoneFormatter


class Marcellis(BaseService):
    @property
    def name(self) -> str:
        return "marcellis.ru"

    @property
    def url(self) -> str:
        return "https://dostavka.marcellis.ru/include/library/SendSMS.php"

    async def send_sms(self) -> Dict[str, Any]:
        formatted_phone = PhoneFormatter.format_with_brackets(self.phone)
        
        data = {
            "phone": formatted_phone
        }

        try:
            response = await self._make_request("POST", self.url, data=data)
            if response.status in [200, 201, 204]:
                return {"success": True, "message": "SMS sent successfully"}
            else:
                return {"success": False, "message": f"Status: {response.status}"}
        except Exception as e:
            return {"success": False, "message": str(e)}

