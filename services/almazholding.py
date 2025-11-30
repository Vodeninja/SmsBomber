from typing import Dict, Any
from core.base_service import BaseService


class Almazholding(BaseService):
    @property
    def name(self) -> str:
        return "almazholding.ru"

    @property
    def url(self) -> str:
        return "https://almazholding.ru/local/user1/sendcode.php"

    async def send_sms(self) -> Dict[str, Any]:
        phone = self._format_phone(self.phone)
        
        data = {
            "PHONE": phone,
            "ECAPTCHA": "undefined"
        }
        headers = {
            "Cookie": "_ym_d=1648577093; _ym_uid=1648577093945352536; PHPSESSID=l8uZ53Njk3Fnh6Sx5k6Fap6hW2CxC42l; ALTASIB_SITETYPE=original; BITRIX_SM_ALMAZ_GUEST_ID=5540491; BITRIX_SM_ALMAZ_LAST_ADV=5_Y; BITRIX_SM_ALMAZ_ALTASIB_LAST_IP=185.100.26.203"
        }

        try:
            response = await self._make_request("POST", self.url, data=data, headers=headers)
            if response.status in [200, 201, 204]:
                return {"success": True, "message": "SMS sent successfully"}
            else:
                return {"success": False, "message": f"Status: {response.status}"}
        except Exception as e:
            return {"success": False, "message": str(e)}

