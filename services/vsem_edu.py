from typing import Dict, Any
from core.base_service import BaseService
from utils import PhoneFormatter


class VsemEdu(BaseService):
    @property
    def name(self) -> str:
        return "vsem-edu-oblako.ru"

    @property
    def url(self) -> str:
        return "https://vsem-edu-oblako.ru/singlemerchant/api/sendconfirmationcode"

    async def send_sms(self) -> Dict[str, Any]:
        formatted_phone = PhoneFormatter.format_with_brackets(self.phone)
        
        params = {
            "lang": "ru",
            "json": "true",
            "merchant_keys": "b27447ba613046d3659f9730ccf15e3c",
            "device_id": "f330883f-b829-41df-83f5-7e263b780e0e",
            "device_platform": "desktop",
            "phone": formatted_phone
        }

        try:
            response = await self._make_request("POST", self.url, params=params)
            if response.status in [200, 201, 204]:
                return {"success": True, "message": "SMS sent successfully"}
            else:
                return {"success": False, "message": f"Status: {response.status}"}
        except Exception as e:
            return {"success": False, "message": str(e)}

