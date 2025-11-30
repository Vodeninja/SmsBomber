from typing import Dict, Any
from core.base_service import BaseService


class RtRu(BaseService):
    @property
    def name(self) -> str:
        return "rt.ru"

    @property
    def url(self) -> str:
        return "https://cnt-vlmr-itv02.svc.iptv.rt.ru/api/v2/portal/send_sms_code"

    async def send_sms(self) -> Dict[str, Any]:
        phone = self._format_phone(self.phone)
        
        data = {
            "action": "register",
            "phone": phone
        }
        headers = {
            "Content-Type": "application/json",
            "session_id": "24f8bbf7-60d3-11ec-b71d-4857027601a0:1951416:2237006:2"
        }

        try:
            response = await self._make_request("POST", self.url, json=data, headers=headers)
            if response.status in [200, 201, 204]:
                return {"success": True, "message": "SMS sent successfully"}
            else:
                return {"success": False, "message": f"Status: {response.status}"}
        except Exception as e:
            return {"success": False, "message": str(e)}

