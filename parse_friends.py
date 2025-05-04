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
            'fields': 'bdate,city,sex,universities'
        }).get('items', None)
        if friends_data is None:
            raise ValueError('Не удалось получить список друзей')
        
        friends = []
        for friend_data in friends_data:
            friend = self._get_friend(friend_data)
            if friend is not None:
                friends.append(friend)

        return friends
    
    def create_graph_by_attr(self, friends: list[Friend], attribute: str):
        if attribute not in ['byear', 'city', 'sex', 'universities']:
            return ValueError(f'Неверный признак: {attribute}')
        
        # создаем узлы графа
        graph = nx.Graph()
        for f in friends:
            f_data = f.get_data()

            f_name = f.name
            f_attr = f_data.get(attribute)
            if f_attr is None:
                continue
            graph.add_node(f_name, attr=f_attr)
        
        # создаем ребра графа
        nodes = graph.nodes(data='attr')
        for i, (name, attr) in enumerate(nodes):
            for j, (other_name, other_attr) in enumerate(nodes):
                if i == j:
                    continue
                if attr == other_attr:
                    graph.add_edge(name, other_name)
        
        return graph


if __name__ == '__main__':
    load_dotenv()
    token = os.environ.get('ACCESS-TOKEN')
    api = Api(token=token)
    friends = api.get_friends()
    for f in friends:
        print(f.get_data())
