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
        friend.update_data(friend_data)

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


    def _get_mutual_friends(self, friend1: Friend, friend2: Friend) -> tuple[Friend, Friend, int]:
        mutual = self.session.method('friends.getMutual', {
            'source_uid': friend1.id,
            'target_uid': friend2.id
        })
        count_mutual = len(mutual)
        return friend1, friend2, count_mutual

    def save_json(self, mutual) -> None:
        result = dict()
        for (k1, k2), v in mutual.items():
            result[','.join((k1, k2))] = v
        
        with open('mutual.json', 'w') as file:
            json.dump(result, file)
    
    def load_json(self) -> dict:
        result = dict()
        with open('mutual.json', 'r') as file:
            data = json.load(file)
            for k, v in data.items():
                k1, k2 = k.split(',')
                result[(k1, k2)] = v
        return result
    
    def get_all_mutual_friends(self, friends: list[Friend]) -> dict[tuple[str, str], int]:
        uids = [str(friend.id) for friend in friends]
        all_mutual = dict()
        for i, uid in enumerate(uids[:-1]):
            print(f'Person {i + 1}/{len(uids)} in process {" " * 10}', end='\r')
            try:
                mutual = self.session.method('friends.getMutual', {
                    'source_uid': uid,
                    'target_uids': ','.join(uids[i + 1:i + 101])
                })
            except:
                continue
            for j, pair in enumerate(mutual, i + 1):
                count = pair.get('common_count') - 1
                if count == 0:
                    continue
                all_mutual[(friends[i].name, friends[j].name)] = count
        
        self.save_json(all_mutual)

        return all_mutual
    

def build_graph(nodes: list[Friend], edges: dict[tuple[str, str], int]) -> None:
    n = [node.name for node in nodes]
    g = nx.Graph()
    g.add_nodes_from(n)
    
    for (p1, p2), w in edges.items():
        g.add_edge(p1, p2, weight=abs(1/w) + 5)
    
    pos = nx.kamada_kawai_layout(g)
    nx.draw(
        g, pos, with_labels=True,
        node_size=200, node_color='lightblue',
        font_size=8, font_weight="bold", edge_color='#c9c9c9'
    )

    plt.show()


if __name__ == '__main__':
    load_dotenv()
    token = os.environ.get('ACCESS-TOKEN')
    api = Api(token=token)
    friends = api.get_friends()
    mutual = api.load_json()
    # for k, v in mutual.items():
    #     print(f'{k}: {v}')
    # mutual = api.get_all_mutual_friends(friends)
    build_graph(friends, mutual)
