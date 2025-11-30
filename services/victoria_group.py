from typing import Dict, Any
from core.base_service import BaseService


class VictoriaGroup(BaseService):
    @property
    def name(self) -> str:
        return "victoria-group.ru"

    @property
    def url(self) -> str:
        return "https://new.victoria-group.ru/api/v2/manzana/Identity/RequestAdvancedPhoneEmailRegistration"

    async def send_sms(self) -> Dict[str, Any]:
        phone = self._format_phone(self.phone)
        
        data = {
            "parameter": {
                "MobilePhone": f"+{phone}",
                "CardNumber": None,
                "AgreeToTerms": 1,
                "AllowNotification": 0
            }
        }
        headers = {
            "Content-Type": "application/json",
            "X-CSRF-TOKEN": "9ZshUjW4iWYuM95Cgo2WmD9pANxDLHGjEOTnOLAA",
            "X-Requested-With": "XMLHttpRequest"
        }

        try:
            response = await self._make_request("POST", self.url, json=data, headers=headers)
            if response.status in [200, 201, 204]:
                return {"success": True, "message": "SMS sent successfully"}
            else:
                return {"success": False, "message": f"Status: {response.status}"}
        except Exception as e:
            return {"success": False, "message": str(e)}

