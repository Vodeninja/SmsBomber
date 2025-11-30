from typing import Dict, Any
from core.base_service import BaseService
from utils import NameGenerator


class Sushiicons(BaseService):
    @property
    def name(self) -> str:
        return "sushiicons.com.ua"

    @property
    def url(self) -> str:
        return "https://sushiicons.com.ua/kiev/index.php?route=common/cart/ajaxgetcoderegister"

    async def send_sms(self) -> Dict[str, Any]:
        phone = self._format_phone(self.phone)
        formatted_phone = phone.replace("380", "+380 (**) ***-**-**", 1) if phone.startswith("380") else phone.replace("7", "+380 (**) ***-**-**", 1)
        firstName = NameGenerator.get_first_name()
        
        data = {
            "firstname": firstName,
            "phone": formatted_phone,
            "birthday": "2005-03-05"
        }

        try:
            response = await self._make_request("POST", self.url, data=data)
            if response.status in [200, 201, 204]:
                return {"success": True, "message": "SMS sent successfully"}
            else:
                return {"success": False, "message": f"Status: {response.status}"}
        except Exception as e:
            return {"success": False, "message": str(e)}

