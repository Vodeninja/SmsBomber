from typing import Dict, Any
from core.base_service import BaseService


class Pickpoint(BaseService):
    @property
    def name(self) -> str:
        return "pickpoint.ru"

    @property
    def url(self) -> str:
        return "https://e-solution.pickpoint.ru/mobileapi/17100/sendsmscode"

    async def send_sms(self) -> Dict[str, Any]:
        phone = self._format_phone(self.phone)
        
        data = {
            "PhoneNumber": phone
        }
        headers = {
            "Content-Type": "application/json",
            "User-Agent": "Application name: pickpoint_android, Android version: 29, Device model: Mi 9T Pro (raphael), App version name: 3.9.0, App version code: 69, App flavor: , Build type: release",
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip"
        }

        try:
            response = await self._make_request("POST", self.url, json=data, headers=headers)
            if response.status in [200, 201, 204]:
                return {"success": True, "message": "SMS sent successfully"}
            else:
                return {"success": False, "message": f"Status: {response.status}"}
        except Exception as e:
            return {"success": False, "message": str(e)}

