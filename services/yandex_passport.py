from typing import Dict, Any
from core.base_service import BaseService


class YandexPassport(BaseService):
    @property
    def name(self) -> str:
        return "yandex.ru"

    @property
    def url(self) -> str:
        return "https://passport.yandex.ru/registration-validations/phone-confirm-code-submit"

    async def send_sms(self) -> Dict[str, Any]:
        phone = self._format_phone(self.phone)
        track_id = self._generate_csrf()[:31]
        
        data = {
            "csrf_token": "",
            "track_id": track_id,
            "display_language": "ru",
            "number": f"+{phone}",
            "confirm_method": "by_sms",
            "isCodeWithFormat": "true"
        }
        headers = {
            "Cookie": "font_loaded=YSv1; is_gdpr=0; is_gdpr_b=COTFARC5cygC; gdpr=0; _ym_uid=1643893010141416800; _ym_d=1652798146; yandexuid=7914983681643893008"
        }

        try:
            response = await self._make_request("POST", self.url, data=data, headers=headers)
            if response.status in [200, 201, 204]:
                return {"success": True, "message": "SMS sent successfully"}
            else:
                return {"success": False, "message": f"Status: {response.status}"}
        except Exception as e:
            return {"success": False, "message": str(e)}

