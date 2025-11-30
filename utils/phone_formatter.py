class PhoneFormatter:
    @staticmethod
    def format(phone: str) -> str:
        phone = phone.replace('+', '').replace(' ', '').replace('-', '').replace('(', '').replace(')', '')
        if phone.startswith('8') and len(phone) == 11:
            phone = '7' + phone[1:]
        return phone

