from typing import Dict, Any
from core.base_service import BaseService
from utils import NameGenerator


class Adengi(BaseService):
    @property
    def name(self) -> str:
        return "adengi.ru"

    @property
    def url(self) -> str:
        return "https://adengi.ru/rest/v1/registration/code/send"

    async def send_sms(self) -> Dict[str, Any]:
        phone = self._format_phone(self.phone)
        firstName = NameGenerator.get_first_name()
        lastName = NameGenerator.get_last_name()
        middleName = NameGenerator.get_first_name()
        email = NameGenerator.get_email()
        
        data = {
            "email": email,
            "firstName": firstName,
            "lastName": lastName,
            "middleName": middleName,
            "phone": phone,
            "via": "sms"
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

