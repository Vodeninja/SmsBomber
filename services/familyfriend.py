from typing import Dict, Any
from core.base_service import BaseService


class Familyfriend(BaseService):
    @property
    def name(self) -> str:
        return "familyfriend.com"

    @property
    def url(self) -> str:
        return "https://familyfriend.com/graphql"

    async def send_sms(self) -> Dict[str, Any]:
        phone = self._format_phone(self.phone)
        
        data = {
            "operationName": "AuthEnterPhoneMutation",
            "query": "mutation AuthEnterPhoneMutation($input: RequestSignInCodeInput!) {\n  result: requestSignInCode(input: $input) {\n    ... on RequestSignInCodePayload {\n      codeLength\n      phone\n      __typename\n    }\n    ... on ErrorPayload {\n      message\n      __typename\n    }\n    __typename\n  }\n}\n",
            "variables": {
                "input": {
                    "phone": phone
                }
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

