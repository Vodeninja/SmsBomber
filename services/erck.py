from typing import Dict, Any
from core.base_service import BaseService
from utils import PhoneFormatter


class Erck(BaseService):
    @property
    def name(self) -> str:
        return "erck.ru"

    @property
    def url(self) -> str:
        return "https://erck.ru/ajax/sms_code.php"

    async def send_sms(self) -> Dict[str, Any]:
        phone = PhoneFormatter.format_compact(self.phone)
        
        params = {
            "action": "send",
            "phone": phone,
            "via_call": "0",
            "registration": "1",
            "prolongation": "0",
            "reset_password": "0",
            "confirm_order": "0",
            "hh": "5b4ca24d86513c145286b68f47848447"
        }
        headers = {
            "Accept": "*/*",
            "Accept-Language": "ru,en;q=0.9,en-GB;q=0.8,en-US;q=0.7",
            "Connection": "keep-alive",
            "Cookie": "PHPSESSID=7mi7b51bpkn3b52lge83cl2n86; utm_source=organic; loan_summ=7000; loan_period=14; _ym_uid=171242747869687122; _ym_d=1712427478; _ym_isad=2; waSessionId=205f56e7-2296-f23f-41db-901c2f7e2174; waUserId_1000131150-dubl_chat_bota_dlya_-1000131150-doc-20944757529=0eb95427-4bbf-e30f-86f5-327735a4728b",
            "Referer": "https://erck.ru/",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "X-Requested-With": "XMLHttpRequest",
            "sec-ch-ua": '"Microsoft Edge";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"'
        }

        try:
            response = await self._make_request("GET", self.url, params=params, headers=headers)
            if response.status in [200, 201, 204]:
                return {"success": True, "message": "SMS sent successfully"}
            else:
                return {"success": False, "message": f"Status: {response.status}"}
        except Exception as e:
            return {"success": False, "message": str(e)}

