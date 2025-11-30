from typing import Dict, Any
from core.base_service import BaseService


class Beerlogapizza(BaseService):
    @property
    def name(self) -> str:
        return "beerlogapizza.ru"

    @property
    def url(self) -> str:
        return "https://beerlogapizza.ru/ajax/global_ajax.php"

    async def send_sms(self) -> Dict[str, Any]:
        phone = self._format_phone(self.phone)
        
        data = {
            "character": "number",
            "phone": phone,
            "code": "",
            "session_id": "e6ab56c6c97b3a47cdee0f60705a8561"
        }

        try:
            response = await self._make_request("POST", self.url, data=data)
            if response.status in [200, 201, 204]:
                return {"success": True, "message": "SMS sent successfully"}
            else:
                return {"success": False, "message": f"Status: {response.status}"}
        except Exception as e:
            return {"success": False, "message": str(e)}

