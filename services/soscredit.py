from typing import Dict, Any
from core.base_service import BaseService


class Soscredit(BaseService):
    @property
    def name(self) -> str:
        return "soscredit.ua"

    @property
    def url(self) -> str:
        return "https://cp.soscredit.ua/graphql/portal"

    async def send_sms(self) -> Dict[str, Any]:
        phone = self._format_phone(self.phone)
        
        data = {
            "operationName": "phoneVerification",
            "variables": {
                "phone": f"+{phone}"
            },
            "query": "mutation phoneVerification($phone: String!) {\n  phoneVerification(phone: $phone)\n}\n"
        }
        headers = {
            "Content-Type": "application/json",
            "Cookie": "lang=uk; device=efe1de42-b98b-454d-a621-347cd7d540b8",
            "Referer": "https://cabinet.soscredit.ua/",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36"
        }

        try:
            response = await self._make_request("POST", self.url, json=data, headers=headers)
            if response.status in [200, 201, 204]:
                return {"success": True, "message": "SMS sent successfully"}
            else:
                return {"success": False, "message": f"Status: {response.status}"}
        except Exception as e:
            return {"success": False, "message": str(e)}

