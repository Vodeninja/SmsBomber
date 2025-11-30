from typing import Dict, Any
from core.base_service import BaseService


class Sravni(BaseService):
    @property
    def name(self) -> str:
        return "sravni.ru"

    @property
    def url(self) -> str:
        return "https://my.sravni.ru/signin/code"

    async def send_sms(self) -> Dict[str, Any]:
        phone = self._format_phone(self.phone)
        
        data = {
            "__RequestVerificationToken": "",
            "phone": f"+{phone}",
            "returnUrl": "/connect/authorize/callback?client_id=www&scope=openid%20offline_access%20email%20phone%20profile%20roles%20reviews%20esia%20orders.r%20messagesender.sms%20Sravni.Reviews.Service%20Sravni.Osago.Service%20Sravni.QnA.Service%20Sravni.FileStorage.Service%20Sravni.PhoneVerifier.Service%20Sravni.Identity.Service%20Sravni.VZR.Service%20Sravni.Affiliates.Service%20Sravni.News.Service&response_type=code%20id_token%20token&redirect_uri=https%3A%2F%2Fwww.sravni.ru%2Fopenid%2Fcallback%2F&response_mode=form_post&state=aKMJO_u7seq0O8Z9swoMZNCxPQII1BQ3BXIcID0uDko&nonce=GmzCt6zbp1YnZf9QHMmPR05NvwI3Cftm5or6YISMk0E&login_hint&acr_values"
        }
        headers = {
            "Cookie": "_ym_uid=1648230902270232651; _ym_d=1652720791; .ASPXANONYMOUS=Wj7EH3nLFEqyHYYidQ77qw; _SL_=6.39.924.2529."
        }

        try:
            response = await self._make_request("POST", self.url, data=data, headers=headers)
            if response.status in [200, 201, 204]:
                return {"success": True, "message": "SMS sent successfully"}
            else:
                return {"success": False, "message": f"Status: {response.status}"}
        except Exception as e:
            return {"success": False, "message": str(e)}

