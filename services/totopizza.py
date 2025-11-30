from typing import Dict, Any
from core.base_service import BaseService
from utils import NameGenerator, PhoneFormatter


class Totopizza(BaseService):
    @property
    def name(self) -> str:
        return "totopizza.ru"

    @property
    def url(self) -> str:
        return "https://api.totopizza.ru/graphql"

    async def send_sms(self) -> Dict[str, Any]:
        formatted_phone = PhoneFormatter.format_no_brackets_spaces(self.phone)
        name = NameGenerator.get_first_name()
        
        data = {
            "operationName": "requestPhoneCodeRegister",
            "query": "\n  mutation requestPhoneCodeRegister($telephone:String! $name:String!) {\n    requestPhoneCodeRegister(input: { telephone:$telephone name:$name })\n  }\n",
            "variables": {
                "name": name,
                "telephone": formatted_phone
            }
        }
        headers = {
            "Content-Type": "application/json"
        }

        try:
            response = await self._make_request("POST", self.url, json=data, headers=headers)
            if response.status in [200, 201, 204]:
                return {"success": True, "message": "SMS sent successfully"}
            else:
                return {"success": False, "message": f"Status: {response.status}"}
        except Exception as e:
            return {"success": False, "message": str(e)}

