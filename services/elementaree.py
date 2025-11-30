from typing import Dict, Any
from core.base_service import BaseService


class Elementaree(BaseService):
    @property
    def name(self) -> str:
        return "elementaree.ru"

    @property
    def url(self) -> str:
        return "https://api-new.elementaree.ru/graphql"

    async def send_sms(self) -> Dict[str, Any]:
        phone = self._format_phone(self.phone)
        
        data = {
            "operationName": "phoneVerification",
            "query": "mutation phoneVerification($phone: String!) {\n  phoneVerification(phone: $phone) {\n    success\n    interval\n    __typename\n  }\n}\n",
            "variables": {
                "phone": phone
            }
        }
        headers = {
            "Content-Type": "application/json"
        }

        try:
            response = await self._make_request("POST", self.url, json=data, headers=headers)
            if response.status in [200, 201, 204]:
                return {"success": True, "message": "SMS sent successfully"}
            else:
                return {"success": False, "message": f"Status: {response.status}"}
        except Exception as e:
            return {"success": False, "message": str(e)}

