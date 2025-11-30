from typing import Dict, Any, Optional
from core.base_service import BaseService


class Onlinedoctor(BaseService):
    @property
    def name(self) -> str:
        return "onlinedoctor.ru"

    @property
    def url(self) -> str:
        return "https://onlinedoctor.ru/mobile/send_sms_code/"
    
    def get_csrf_url(self) -> Optional[str]:
        return "https://onlinedoctor.ru/doctors/"

    async def send_sms(self) -> Dict[str, Any]:
        phone = self._format_phone(self.phone)
        
        data = {
            "phone": phone
        }
        headers = {
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Accept-Language": "ru,en;q=0.9,en-GB;q=0.8,en-US;q=0.7",
            "Connection": "keep-alive",
            "Cookie": "_ym_uid=1704726654816896240; _ym_d=1704726654; SESSID=6m88pkjltved2mcv183dt5520a; timeout_tz=1; check_city_shown=1; _ym_isad=2; _ym_visorc=w",
            "Origin": "https://onlinedoctor.ru",
            "Referer": "https://onlinedoctor.ru/doctors/",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "X-CSRFToken": "",
            "X-Requested-With": "XMLHttpRequest",
            "sec-ch-ua": '"Microsoft Edge";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"'
        }

        try:
            response = await self._make_request("POST", self.url, data=data, headers=headers)
            if response.status in [200, 201, 204]:
                return {"success": True, "message": "SMS sent successfully"}
            else:
                return {"success": False, "message": f"Status: {response.status}"}
        except Exception as e:
            return {"success": False, "message": str(e)}

