from typing import Dict, Any, Optional
from core.base_service import BaseService
from utils import PhoneFormatter


class Valta(BaseService):
    @property
    def name(self) -> str:
        return "valta.ru"

    @property
    def url(self) -> str:
        return "https://valta.ru/bitrix/services/main/ajax.php"
    
    def get_csrf_url(self) -> Optional[str]:
        return "https://valta.ru/register/current_client/person/private_zooservis/"

    async def send_sms(self) -> Dict[str, Any]:
        phone = PhoneFormatter.format_with_spaces(self.phone)
        
        params = {
            "mode": "class",
            "c": "citfact:register",
            "action": "sendSms"
        }
        data = {
            "phone": phone
        }
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "accept": "*/*",
            "accept-language": "ru,en;q=0.9,en-GB;q=0.8,en-US;q=0.7",
            "bx-ajax": "true",
            "content-type": "application/x-www-form-urlencoded",
            "cookie": "PHPSESSID=8cz2BriEXrv3rfoi9CR0vpBdKeQKqJI4; BITRIX_SM_GUEST_ID=2616248; BITRIX_SM_LAST_ADV=5_Y; BITRIX_SM_SALE_UID=21754426; BITRIX_CONVERSION_CONTEXT_s1=%7B%22ID%22%3A20%2C%22EXPIRE%22%3A1712437140%2C%22UNIQUE%22%3A%5B%22conversion_visit_day%22%5D%7D; _gid=GA1.2.85549300.1712421751; _gat_gtag_UA_52444218_17=1; BX_USER_ID=104ae4c8487577c4433d7aed32dfbf92; _ym_uid=1712421751125857632; _ym_d=1712421751; _ym_isad=2; _ym_visorc=w; cookie_notify=showed; BITRIX_SM_LAST_VISIT=06.04.2024%2019%3A42%3A56; _ga_4ESKKEVKD6=GS1.1.1712421751.1.1.1712421781.30.0.0; _ga=GA1.2.1144781229.1712421751",
            "origin": "https://valta.ru",
            "referer": "https://valta.ru/register/current_client/person/private_zooservis/",
            "sec-ch-ua": '"Microsoft Edge";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 Edg/123.0.0.0",
            "x-bitrix-csrf-token": "",
            "x-bitrix-site-id": "s1"
        }

        try:
            response = await self._make_request("POST", self.url, params=params, data=data, headers=headers)
            if response.status in [200, 201, 204]:
                return {"success": True, "message": "SMS sent successfully"}
            else:
                return {"success": False, "message": f"Status: {response.status}"}
        except Exception as e:
            return {"success": False, "message": str(e)}

