from typing import Dict, Any, Optional
from core.base_service import BaseService
from utils import NameGenerator


class Rozetka(BaseService):
    @property
    def name(self) -> str:
        return "rozetka.com.ua"

    @property
    def url(self) -> str:
        return "https://uss.rozetka.com.ua/session/auth/signup-phone"
    
    def get_csrf_url(self) -> Optional[str]:
        return "https://uss.rozetka.com.ua/"

    async def send_sms(self) -> Dict[str, Any]:
        phone = self._format_phone(self.phone)
        firstName = NameGenerator.get_first_name()
        lastName = NameGenerator.get_last_name()
        email = NameGenerator.get_email()
        
        data = {
            "title": firstName,
            "first_name": firstName,
            "last_name": lastName,
            "password": NameGenerator.get_first_name() + "A123",
            "email": email,
            "phone": phone,
            "request_token": "rB4eDGHMb00wHeQls7l4Ag=="
        }
        headers = {
            "Cookie": "ab-cart-se=new; xab_segment=123; slang=ru; uid=rB4eDGHMb00wHeQls7l4Ag==; visitor_city=1; _uss-csrf=",
            "Csrf-Token": ""
        }

        try:
            response = await self._make_request("POST", self.url, data=data, headers=headers)
            if response.status in [200, 201, 204]:
                return {"success": True, "message": "SMS sent successfully"}
            else:
                return {"success": False, "message": f"Status: {response.status}"}
        except Exception as e:
            return {"success": False, "message": str(e)}

