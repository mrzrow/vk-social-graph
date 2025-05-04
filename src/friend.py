from typing import Any


# Класс друга
class Friend:
    def __init__(self):
        # Необходимые поля
        self.id: int | None = None
        self.first_name: str | None = None
        self.last_name: str | None = None
        self.byear: int | None = None
        self.sex: str | None = None
        self.universities: list[int] = []
    
    # Свойство, которое позволяет получить имя человека
    @property
    def name(self):
        return ' '.join((self.first_name, self.last_name))
    
    # Свойство, которое позволят понять, удален ли аккаунт
    @property
    def is_deleted(self):
        return self.first_name == 'DELETED'

    # Получение данных о друге из запроса
    def set_data(self, data: dict[str, Any]) -> None:
        self.id = data.get('id')

        self.first_name = data.get('first_name')
        self.last_name = data.get('last_name')

        bdate = data.get('bdate')
        if bdate is not None:
            bdate_split = bdate.split('.')
            if len(bdate_split) == 3:
                self.byear = int(bdate_split[-1])

        all_sex = {0: None, 1: 'Женский', 2: 'Мужской'}
        sex = data.get('sex', 0)
        self.sex = all_sex.get(sex)

        self.city = data.get('city')
        if self.city is not None:
            self.city = self.city.get('title')

        universities_data = data.get('universities', [])
        if universities_data:
            for uni in universities_data:
                self.universities.append(uni.get('name'))
    
    # Возваращение данных в виде словаря
    def get_data(self) -> dict[str, Any]:
        return {
            'id': self.id,
            'name': self.name,
            'byear': self.byear,
            'city': self.city,
            'sex': self.sex,
            'universities': self.universities,
        }
