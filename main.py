import os
from dotenv import load_dotenv

from src import Api, Graph


if __name__ == '__main__':
    load_dotenv()
    token = os.environ.get('ACCESS-TOKEN')

    vk = Api(token=token)
    gr = Graph()
    
    try:
        user_id = int(input('Введите свой ID пользователя: '))
    except ValueError:
        raise ValueError('ID пользователя должен являться числом')
    
    attribute = input('Введите признак, по которому будет строится граф: ')
    
    friends = vk.get_friends(user_id=user_id)
    gr.plot_graph(friends=friends, attribute=attribute)

