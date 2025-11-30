from typing import Dict, Any
from core.base_service import BaseService


class Yaro(BaseService):
    @property
    def name(self) -> str:
        return "yaro.ua"

    @property
    def url(self) -> str:
        return "https://yaro.ua/assets/components/office/action.php"

    async def send_sms(self) -> Dict[str, Any]:
        phone = self._format_phone(self.phone)
        
        data = {
            "action": "authcustom/formRegister",
            "mobilephone": phone,
            "pageId": "116",
            "csrf": "b1618ecce3d6e49833f9d9c8c93f9c53"
        }

        try:
            response = await self._make_request("POST", self.url, data=data)
            if response.status in [200, 201, 204]:
                return {"success": True, "message": "SMS sent successfully"}
            else:
                return {"success": False, "message": f"Status: {response.status}"}
        except Exception as e:
            return {"success": False, "message": str(e)}

