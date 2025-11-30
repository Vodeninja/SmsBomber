from typing import Dict, Any
from core.base_service import BaseService
from utils import NameGenerator


class Welldonego(BaseService):
    @property
    def name(self) -> str:
        return "welldonego.ru"

    @property
    def url(self) -> str:
        return "https://openapi.welldonego.ru/api/v1/user/create"

    async def send_sms(self) -> Dict[str, Any]:
        phone = self._format_phone(self.phone)
        firstName = NameGenerator.get_first_name()
        lastName = NameGenerator.get_last_name()
        
        data = {
            "firstName": firstName,
            "lastName": lastName,
            "msisdn": phone,
            "offerAccepted": True
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

