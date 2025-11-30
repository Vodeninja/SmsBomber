from typing import Dict, Any
from core.base_service import BaseService
from utils import NameGenerator, PhoneFormatter


class Stockmann(BaseService):
    @property
    def name(self) -> str:
        return "stockmann.ru"

    @property
    def url(self) -> str:
        return "https://stockmann.ru/ajax/"

    async def send_sms(self) -> Dict[str, Any]:
        formatted_phone = PhoneFormatter.format_spaces_around_dashes(self.phone)
        firstName = NameGenerator.get_first_name()
        lastName = NameGenerator.get_last_name()
        email = NameGenerator.get_email()
        
        params = {
            "controller": "user",
            "action": "registerUser",
            "surname": lastName,
            "name": firstName,
            "phone": formatted_phone,
            "email": email,
            "password": "qwerty",
            "password_confirm": "qwerty"
        }

        try:
            response = await self._make_request("POST", self.url, params=params)
            if response.status in [200, 201, 204]:
                return {"success": True, "message": "SMS sent successfully"}
            else:
                return {"success": False, "message": f"Status: {response.status}"}
        except Exception as e:
            return {"success": False, "message": str(e)}

