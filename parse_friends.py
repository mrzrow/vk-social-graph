import os
from typing import Any

import vk_api
import networkx as nx
import plotly.graph_objects as go
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
            raise ValueError(f'Неверный признак: {attribute}')
        
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

    def plot_graph(self, raph: nx.Graph):
        pos = nx.spring_layout(graph)

        edge_x, edge_y = [], []
        for edge0, edge1 in graph.edges():
            x0, y0 = pos[edge0]
            x1, y1 = pos[edge1]
            edge_x.extend([x0, x1])
            edge_y.extend([y0, y1])

        node_x, node_y = [], []
        node_name = []
        for node in graph.nodes():
            x, y = pos[node]
            node_x.append(x)
            node_y.append(y)
            node_name.append(node)
        
        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=edge_x, y=edge_y,
            line={'width': 0.5, 'color': 'gray'},
            hoverinfo=None,
            mode='lines'
        ))

        fig.add_trace(go.Scatter(
            x=node_x, y=node_y,
            mode='markers',
            hoverinfo='text',
            text=node_name,
            marker={
                'symbol': 'circle',
                'size': 10,
                'color': 'blue',
                'line': {
                    'width': 2,
                    'color': 'black',
                },
            }
        ))

        fig.update_layout(
            title='vk-social-graph',
            showlegend=False,
            height=800,
            width=800,
            title_x=0.5,
            title_y=0.95
        )
        return fig


if __name__ == '__main__':
    load_dotenv()
    token = os.environ.get('ACCESS-TOKEN')
    api = Api(token=token)
    friends = api.get_friends()
    graph = api.create_graph_by_attr(friends, 'byear')
    fig = api.plot_graph(graph)
    fig.show()
