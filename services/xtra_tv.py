from typing import Dict, Any
from core.base_service import BaseService


class XtraTv(BaseService):
    @property
    def name(self) -> str:
        return "xtra.tv"

    @property
    def url(self) -> str:
        return "https://my.xtra.tv/api/signup?lang=uk"

    async def send_sms(self) -> Dict[str, Any]:
        phone = self._format_phone(self.phone)
        
        data = {
            "phone": f"+{phone}"
        }
        headers = {
            "Cookie": "sessionId=93m23ha15pdhgq0mmlea9lneg2; _ga=GA1.2.1745043441.1634385834",
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36"
        }

        try:
            response = await self._make_request("POST", self.url, data=data, headers=headers)
            if response.status in [200, 201, 204]:
                return {"success": True, "message": "SMS sent successfully"}
            else:
                return {"success": False, "message": f"Status: {response.status}"}
        except Exception as e:
            return {"success": False, "message": str(e)}

