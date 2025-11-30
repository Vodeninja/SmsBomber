from typing import Dict, Any
from core.base_service import BaseService


class VodovozSpb(BaseService):
    @property
    def name(self) -> str:
        return "vodovoz-spb.ru"

    @property
    def url(self) -> str:
        return "https://shop.vodovoz-spb.ru/bitrix/tools/ajax_sms.php"

    async def send_sms(self) -> Dict[str, Any]:
        phone = self._format_phone(self.phone)
        formatted_phone = phone.replace("7", "+7 (", 1)[:2] + "***) ***-**-**"
        
        data = {
            "phone": formatted_phone
        }

        try:
            response = await self._make_request("POST", self.url, data=data)
            if response.status in [200, 201, 204]:
                return {"success": True, "message": "SMS sent successfully"}
            else:
                return {"success": False, "message": f"Status: {response.status}"}
        except Exception as e:
            return {"success": False, "message": str(e)}

