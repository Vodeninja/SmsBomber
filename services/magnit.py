from typing import Dict, Any
from core.base_service import BaseService


class Magnit(BaseService):
    @property
    def name(self) -> str:
        return "magnit.ru"

    @property
    def url(self) -> str:
        return "https://new.moy.magnit.ru/local/ajax/login/"

    async def send_sms(self) -> Dict[str, Any]:
        phone = self._format_phone(self.phone)
        formatted_phone = phone.replace("7", "+ 7 ( *** ) ***-**-**", 1)
        
        data = {
            "phone": formatted_phone,
            "ksid": "ad040b9d-df39-4e88-9c6c-10e6ba6ffbc6_0"
        }

        try:
            response = await self._make_request("POST", self.url, data=data)
            if response.status in [200, 201, 204]:
                return {"success": True, "message": "SMS sent successfully"}
            else:
                return {"success": False, "message": f"Status: {response.status}"}
        except Exception as e:
            return {"success": False, "message": str(e)}

