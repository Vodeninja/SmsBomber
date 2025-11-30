from typing import Dict, Any
from core.base_service import BaseService
from utils import NameGenerator


class all_cars_ufa(BaseService):
    @property
    def name(self) -> str:
        return "all-cars-ufa.ru"

    @property
    def url(self) -> str:
        return "https://all-cars-ufa.ru/api/lead"

    async def send_sms(self) -> Dict[str, Any]:
        phone = self._format_phone(self.phone)
        name = NameGenerator.get_first_last()

        data = {
            "name": name,
            "phone": phone,
            "url": "https://all-cars-ufa.ru/catalog/moskvich/moskvich_61",
            "useragent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36",
            "url_params": {
                "utm_campaign": "704477190||рсф фид уфа",
                "utm_content": "yandex.ru",
                "utm_medium": "cpc",
                "utm_source": "yandexrsyDD",
                "utm_term": "---autotargeting||205672916962",
                "yclid": "",
                "ad_id": "",
                "banner_id": "1891638076880726325",
                "ybaip": "1",
            },
            "car_brand": "Москвич",
            "car_model": "6",
            "car_compl": "1.5 CVT (136 л.с.) Комфорт",
            "car_price": "1 100 000 ₽",
            "comment": "Есть авто на обмен по трейд-ин",
            "source": "car",
        }
        headers = {
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        }

        try:
            response = await self._make_request(
                "POST", self.url, json=data, headers=headers
            )

            if response.status in [200, 201, 204]:
                return {"success": True, "message": "SMS sent successfully"}
            else:
                return {"success": False, "message": f"Status: {response.status}"}
        except Exception as e:
            return {"success": False, "message": str(e)}
