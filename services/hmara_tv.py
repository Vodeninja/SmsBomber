from typing import Dict, Any
from core.base_service import BaseService


class HmaraTv(BaseService):
    @property
    def name(self) -> str:
        return "hmara.tv"

    @property
    def url(self) -> str:
        return "https://my.hmara.tv/api/sign"

    async def send_sms(self) -> Dict[str, Any]:
        phone = self._format_phone(self.phone)
        
        params = {
            "contact": phone,
            "deviceId": "81826091-f299-4515-b70f-e82fd00fec9a",
            "language": "ru",
            "profileId": "1",
            "deviceType": "2",
            "ver": "2.2.9"
        }
        headers = {
            "Cookie": "_ga=GA1.2.641734216.1650994527; _gid=GA1.2.109748838.1650994527"
        }

        try:
            response = await self._make_request("POST", self.url, params=params, headers=headers)
            if response.status in [200, 201, 204]:
                return {"success": True, "message": "SMS sent successfully"}
            else:
                return {"success": False, "message": f"Status: {response.status}"}
        except Exception as e:
            return {"success": False, "message": str(e)}

