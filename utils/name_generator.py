import random


class NameGenerator:
    FIRST_NAMES = [
        'Александр', 'Дмитрий', 'Максим', 'Сергей', 'Андрей', 'Алексей', 'Артем',
        'Илья', 'Кирилл', 'Михаил', 'Никита', 'Матвей', 'Роман', 'Егор',
        'Арсений', 'Иван', 'Денис', 'Евгений', 'Тимофей', 'Владислав',
        'Анна', 'Мария', 'Елена', 'Ольга', 'Татьяна', 'Наталья', 'Ирина',
        'Светлана', 'Екатерина', 'Юлия', 'Анастасия', 'Дарья', 'Виктория',
        'Полина', 'София', 'Александра', 'Василиса', 'Вероника', 'Арина'
    ]
    
    LAST_NAMES = [
        'Иванов', 'Петров', 'Сидоров', 'Смирнов', 'Кузнецов', 'Попов', 'Соколов',
        'Лебедев', 'Козлов', 'Новиков', 'Морозов', 'Петров', 'Волков', 'Соловьев',
        'Васильев', 'Зайцев', 'Павлов', 'Семенов', 'Голубев', 'Виноградов',
        'Богданов', 'Воробьев', 'Федоров', 'Михайлов', 'Белов', 'Тарасов',
        'Беляев', 'Комаров', 'Орлов', 'Киселев', 'Макаров', 'Андреев'
    ]
    
    MIDDLE_NAMES = [
        'Александрович', 'Дмитриевич', 'Максимович', 'Сергеевич', 'Андреевич',
        'Алексеевич', 'Артемович', 'Ильич', 'Кириллович', 'Михайлович',
        'Никитич', 'Матвеевич', 'Романович', 'Егорович', 'Арсеньевич',
        'Иванович', 'Денисович', 'Евгеньевич', 'Тимофеевич', 'Владиславович',
        'Александровна', 'Дмитриевна', 'Максимовна', 'Сергеевна', 'Андреевна',
        'Алексеевна', 'Артемовна', 'Ильинична', 'Кирилловна', 'Михайловна',
        'Никитична', 'Матвеевна', 'Романовна', 'Егоровна', 'Арсеньевна',
        'Ивановна', 'Денисовна', 'Евгеньевна', 'Тимофеевна', 'Владиславовна'
    ]
    
    @classmethod
    def get_first_name(cls) -> str:
        return random.choice(cls.FIRST_NAMES)
    
    @classmethod
    def get_last_name(cls) -> str:
        return random.choice(cls.LAST_NAMES)
    
    @classmethod
    def get_middle_name(cls, first_name: str = None) -> str:
        if first_name:
            is_female = first_name.endswith('а') or first_name.endswith('я')
            middle_names = [m for m in cls.MIDDLE_NAMES if m.endswith('на' if is_female else 'ч')]
            return random.choice(middle_names) if middle_names else random.choice(cls.MIDDLE_NAMES)
        return random.choice(cls.MIDDLE_NAMES)
    
    @classmethod
    def get_full_name(cls) -> str:
        first = cls.get_first_name()
        last = cls.get_last_name()
        middle = cls.get_middle_name(first)
        return f"{last} {first} {middle}"
    
    @classmethod
    def get_first_last(cls) -> str:
        return f"{cls.get_first_name()} {cls.get_last_name()}"
    
    @classmethod
    def get_email(cls) -> str:
        first = cls.get_first_name().lower()
        last = cls.get_last_name().lower()
        domains = ['gmail.com', 'mail.ru', 'yandex.ru', 'rambler.ru', 'hotmail.com']
        return f"{first}.{last}@{random.choice(domains)}"

