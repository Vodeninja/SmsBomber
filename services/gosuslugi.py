from typing import Dict, Any
from core.base_service import BaseService
from utils import NameGenerator, PhoneFormatter


class Gosuslugi(BaseService):
    @property
    def name(self) -> str:
        return "gosuslugi.ru"

    @property
    def url(self) -> str:
        return "https://www.gosuslugi.ru/auth-provider/mobile/register"

    async def send_sms(self) -> Dict[str, Any]:
        formatted_phone = PhoneFormatter.format_no_dashes(self.phone)
        firstName = NameGenerator.get_first_name()
        lastName = NameGenerator.get_last_name()
        
        data = {
            "instanceId": "123",
            "firstName": firstName,
            "lastName": lastName,
            "contactType": "mobile",
            "contactValue": formatted_phone
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

