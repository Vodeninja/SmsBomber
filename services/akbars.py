from typing import Dict, Any
from core.base_service import BaseService


class Akbars(BaseService):
    @property
    def name(self) -> str:
        return "akbars.ru"

    @property
    def url(self) -> str:
        return "https://www.akbars.ru/api/PhoneConfirm/"

    async def send_sms(self) -> Dict[str, Any]:
        phone = self._format_phone(self.phone)
        
        data = {
            "phoneNumber": phone
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

