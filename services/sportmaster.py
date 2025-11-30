from typing import Dict, Any
from core.base_service import BaseService


class Sportmaster(BaseService):
    @property
    def name(self) -> str:
        return "sportmaster.ua"

    @property
    def url(self) -> str:
        return "https://www.sportmaster.ua/?module=users&action=SendSMSReg"

    async def send_sms(self) -> Dict[str, Any]:
        phone = self._format_phone(self.phone)
        
        params = {
            "phone": phone
        }

        try:
            response = await self._make_request("POST", self.url, params=params)
            if response.status in [200, 201, 204]:
                return {"success": True, "message": "SMS sent successfully"}
            else:
                return {"success": False, "message": f"Status: {response.status}"}
        except Exception as e:
            return {"success": False, "message": str(e)}

