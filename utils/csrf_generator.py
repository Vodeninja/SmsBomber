import random
import string
import hashlib
import time
import base64


class CSRFGenerator:
    @staticmethod
    def generate_hex(length: int = 32) -> str:
        return ''.join(random.choices(string.hexdigits, k=length))
    
    @staticmethod
    def generate_base64(length: int = 32) -> str:
        random_bytes = ''.join(random.choices(string.ascii_letters + string.digits, k=length)).encode()
        return base64.b64encode(random_bytes).decode()[:length]
    
    @staticmethod
    def generate_alphanumeric(length: int = 32) -> str:
        return ''.join(random.choices(string.ascii_letters + string.digits, k=length))
    
    @staticmethod
    def generate_with_timestamp(length: int = 24) -> str:
        timestamp = str(int(time.time()))
        random_part = ''.join(random.choices(string.hexdigits, k=length - len(timestamp)))
        return timestamp + random_part
    
    @staticmethod
    def generate_hash_based(seed: str = None) -> str:
        if seed is None:
            seed = str(time.time()) + ''.join(random.choices(string.ascii_letters, k=10))
        hash_obj = hashlib.md5(seed.encode())
        return hash_obj.hexdigest()
    
    @staticmethod
    def generate_bitrix_format() -> str:
        return ''.join(random.choices(string.hexdigits.lower(), k=32))
    
    @staticmethod
    def generate_yandex_format() -> str:
        random_part = ''.join(random.choices(string.hexdigits, k=40))
        timestamp = str(int(time.time()))
        return f"{random_part}:{timestamp}"
    
    @staticmethod
    def generate_django_format() -> str:
        random_part = ''.join(random.choices(string.ascii_letters + string.digits, k=64))
        return random_part
    
    @staticmethod
    def generate_laravel_format() -> str:
        random_bytes = ''.join(random.choices(string.ascii_letters + string.digits, k=40)).encode()
        return base64.b64encode(random_bytes).decode()
    
    @staticmethod
    def generate_custom(pattern: str) -> str:
        result = []
        for char in pattern:
            if char == 'x':
                result.append(random.choice(string.hexdigits))
            elif char == 'a':
                result.append(random.choice(string.ascii_letters))
            elif char == 'd':
                result.append(random.choice(string.digits))
            elif char == 'A':
                result.append(random.choice(string.ascii_letters + string.digits))
            else:
                result.append(char)
        return ''.join(result)

