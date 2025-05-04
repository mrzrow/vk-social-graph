import os
import json
from typing import Any

import vk_api
import networkx as nx
import matplotlib.pyplot as plt
from dotenv import load_dotenv

from friend import Friend


class Api:
    def __init__(self, token: str):
        self.token = token
        self.session = vk_api.VkApi(token=token)

    def _get_friend(self, friend_data: dict[str, Any]) -> Friend | None:
        friend = Friend()
        friend.set_data(friend_data)

        if friend.is_deleted:
            return None
        return friend
        

    def get_friends(self, user_id=None) -> list[Friend]:

        friends_data: list | None = self.session.method('friends.get', {
            'user_id': user_id,
            'order': 'name',
            'fields': 'bdate,sex,city,universities'
        }).get('items', None)
        if friends_data is None:
            raise ValueError
        
        friends = []
        for friend_data in friends_data:
            friend = self._get_friend(friend_data)
            if friend is not None:
                friends.append(friend)

        return friends


if __name__ == '__main__':
    load_dotenv()
    token = os.environ.get('ACCESS-TOKEN')
    api = Api(token=token)
    friends = api.get_friends()
