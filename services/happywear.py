from typing import Dict, Any
from core.base_service import BaseService
from utils import NameGenerator, PhoneFormatter


class Happywear(BaseService):
    @property
    def name(self) -> str:
        return "happywear.ru"

    @property
    def url(self) -> str:
        return "https://happywear.ru/index.php?route=module/registerformbox/ajaxCheckEmail"

    async def send_sms(self) -> Dict[str, Any]:
        formatted_phone = PhoneFormatter.format_no_plus_brackets(self.phone)
        email = NameGenerator.get_email()
        
        data = {
            "email": email,
            "telephone": formatted_phone,
            "password": "qVVwa6QwcaCPP2s",
            "confirm": "qVVwa6QwcaCPP2s"
        }

        try:
            response = await self._make_request("POST", self.url, data=data)
            if response.status in [200, 201, 204]:
                return {"success": True, "message": "SMS sent successfully"}
            else:
                return {"success": False, "message": f"Status: {response.status}"}
        except Exception as e:
            return {"success": False, "message": str(e)}

