from typing import Dict, Any
from core.base_service import BaseService


class Bandeatos(BaseService):
    @property
    def name(self) -> str:
        return "bandeatos.ru"

    @property
    def url(self) -> str:
        return "https://bandeatos.ru/?MODE=AJAX"

    async def send_sms(self) -> Dict[str, Any]:
        phone = self._format_phone(self.phone)
        
        data = {
            "sessid": "404d33f8bac1c1aa4305e6af3ebffa8b",
            "FORM_ID": "bx_1789522556_form",
            "PHONE_NUMBER": f"+{phone}"
        }

        try:
            response = await self._make_request("POST", self.url, data=data)
            if response.status in [200, 201, 204]:
                return {"success": True, "message": "SMS sent successfully"}
            else:
                return {"success": False, "message": f"Status: {response.status}"}
        except Exception as e:
            return {"success": False, "message": str(e)}

