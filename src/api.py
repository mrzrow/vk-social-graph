import vk_api
from typing import Any

from .friend import Friend


# Класс по взаимодействию с API ВКонтакте
class Api:
    # Инициализация: получение токена
    def __init__(self, token: str):
        self.token = token
        self.session = vk_api.VkApi(token=token)

    # Вспомогательный метод для получения списка друзей
    def _get_friend(self, friend_data: dict[str, Any]) -> Friend | None:
        friend = Friend()
        friend.set_data(friend_data)

        if friend.is_deleted:
            return None
        return friend
        
    # Получение списка друзей
    def get_friends(self, user_id=None) -> list[Friend]:
        # Запрос к API ВКонтакте
        friends_data: list | None = self.session.method('friends.get', {
            'user_id': user_id,
            'order': 'name',
            'fields': 'bdate,city,sex,universities'
        }).get('items', None)
        if friends_data is None:
            raise ValueError('Не удалось получить список друзей')
        
        # Формирование списка друзей
        friends = []
        for friend_data in friends_data:
            friend = self._get_friend(friend_data)
            if friend is not None:
                friends.append(friend)

        return friends
