from typing import Dict, Any
from core.base_service import BaseService
from utils import PhoneFormatter


class Zdesapteka(BaseService):
    @property
    def name(self) -> str:
        return "zdesapteka.ru"

    @property
    def url(self) -> str:
        return "https://zdesapteka.ru/bitrix/services/main/ajax.php?action=zs%3Amain.ajax.AuthActions.sendAuthCode"

    async def send_sms(self) -> Dict[str, Any]:
        formatted_phone = PhoneFormatter.format_with_brackets(self.phone)
        
        data = {
            "userPhone": formatted_phone,
            "SITE_ID": "s1",
            "sessid": ""
        }

        try:
            response = await self._make_request("POST", self.url, data=data)
            if response.status in [200, 201, 204]:
                return {"success": True, "message": "SMS sent successfully"}
            else:
                return {"success": False, "message": f"Status: {response.status}"}
        except Exception as e:
            return {"success": False, "message": str(e)}

