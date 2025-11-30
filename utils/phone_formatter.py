class PhoneFormatter:
    @staticmethod
    def format(phone: str) -> str:
        phone = phone.replace('+', '').replace(' ', '').replace('-', '').replace('(', '').replace(')', '')
        if phone.startswith('8') and len(phone) == 11:
            phone = '7' + phone[1:]
        return phone
    
    @staticmethod
    def format_full(phone: str) -> str:
        return PhoneFormatter.format(phone)
    
    @staticmethod
    def format_with_spaces(phone: str) -> str:
        phone = PhoneFormatter.format(phone)
        if len(phone) == 11:
            return f"+7 {phone[1:4]} {phone[4:7]} {phone[7:9]}-{phone[9:11]}"
        return phone
    
    @staticmethod
    def format_with_brackets(phone: str) -> str:
        phone = PhoneFormatter.format(phone)
        if len(phone) == 11:
            return f"+7 ({phone[1:4]}) {phone[4:7]}-{phone[7:9]}-{phone[9:11]}"
        return phone
    
    @staticmethod
    def format_compact(phone: str) -> str:
        phone = PhoneFormatter.format(phone)
        if len(phone) == 11:
            return f"+7({phone[1:4]}){phone[4:7]}-{phone[7:11]}"
        return phone
    
    @staticmethod
    def format_brackets_only(phone: str) -> str:
        phone = PhoneFormatter.format(phone)
        if len(phone) == 11:
            return f"({phone[1:4]}){phone[4:7]}-{phone[7:9]}-{phone[9:11]}"
        return phone
    
    @staticmethod
    def format_no_plus_brackets(phone: str) -> str:
        phone = PhoneFormatter.format(phone)
        if len(phone) == 11:
            return f"7({phone[1:4]}){phone[4:7]}-{phone[7:9]}-{phone[9:11]}"
        return phone
    
    @staticmethod
    def format_spaces_around_dashes(phone: str) -> str:
        phone = PhoneFormatter.format(phone)
        if len(phone) == 11:
            return f"+7 ({phone[1:4]}) {phone[4:7]} - {phone[7:9]} - {phone[9:11]}"
        return phone
    
    @staticmethod
    def format_all_spaces(phone: str) -> str:
        phone = PhoneFormatter.format(phone)
        if len(phone) == 11:
            return f"+ 7 ( {phone[1:4]} ) {phone[4:7]}-{phone[7:9]}-{phone[9:11]}"
        return phone
    
    @staticmethod
    def format_no_space_after_bracket(phone: str) -> str:
        phone = PhoneFormatter.format(phone)
        if len(phone) == 11:
            return f"+7 ({phone[1:4]}){phone[4:7]}-{phone[7:9]}-{phone[9:11]}"
        return phone
    
    @staticmethod
    def format_no_dashes(phone: str) -> str:
        phone = PhoneFormatter.format(phone)
        if len(phone) == 11:
            return f"+7({phone[1:4]}){phone[4:7]}{phone[7:11]}"
        return phone
    
    @staticmethod
    def format_no_brackets_spaces(phone: str) -> str:
        phone = PhoneFormatter.format(phone)
        if len(phone) == 11:
            return f"+7 {phone[1:4]} {phone[4:7]} {phone[7:9]} {phone[9:11]}"
        return phone
    
    @staticmethod
    def format_ukrainian(phone: str) -> str:
        phone = PhoneFormatter.format(phone)
        if phone.startswith('380') and len(phone) == 12:
            return f"+380 ({phone[3:5]}) {phone[5:8]}-{phone[8:10]}-{phone[10:12]}"
        elif len(phone) == 11:
            return f"+380 ({phone[1:3]}) {phone[3:6]}-{phone[6:8]}-{phone[8:10]}"
        return phone

