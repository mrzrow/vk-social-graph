import networkx as nx
import plotly.graph_objects as go

from .friend import Friend

class Graph:
    def _is_attr_connected(self, attr1: str | int | list, attr2: str | int | list) -> bool:
        if not (isinstance(attr1, list) and isinstance(attr2, list)):
            return attr1 == attr2
        return bool(set(attr1) & set(attr2))

    def _create_graph_by_attr(self, friends: list[Friend], attribute: str) -> nx.Graph:
        if attribute not in ['byear', 'city', 'sex', 'universities']:
            raise ValueError(f'Неверный признак: {attribute}')
        
        # создаем узлы графа
        graph = nx.Graph()
        for f in friends:
            f_data = f.get_data()

            f_name = f_data.get('name')
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
                if self._is_attr_connected(attr, other_attr):
                    graph.add_edge(name, other_name)
        
        return graph

    def plot_graph(self, friends: list[Friend], attribute: str) -> go.Figure:
        graph = self._create_graph_by_attr(friends=friends, attribute=attribute)
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
        
        fig.show()
    