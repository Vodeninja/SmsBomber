from typing import Dict, Any, Optional
from core.base_service import BaseService


class Mrroll(BaseService):
    @property
    def name(self) -> str:
        return "mrroll.ru"

    @property
    def url(self) -> str:
        return "http://mrroll.ru/user/signin"
    
    def get_csrf_url(self) -> Optional[str]:
        return "http://mrroll.ru/user/signin"

    async def send_sms(self) -> Dict[str, Any]:
        phone = self._format_phone(self.phone)
        formatted_phone = phone.replace("7", "(***)***-**-**", 1)
        
        data = {
            "_csrf": "",
            "User[phone]": formatted_phone,
            "step": "send-sms"
        }
        headers = {
            "X-CSRF-Token": "",
            "X-Requested-With": "XMLHttpRequest"
        }

        try:
            response = await self._make_request("POST", self.url, data=data, headers=headers)
            if response.status in [200, 201, 204]:
                return {"success": True, "message": "SMS sent successfully"}
            else:
                return {"success": False, "message": f"Status: {response.status}"}
        except Exception as e:
            return {"success": False, "message": str(e)}

