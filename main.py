import os
from dotenv import load_dotenv

from src import Api, Graph


if __name__ == '__main__':
    # Получаем переменную ACCESS-TOKEN из переменных среды
    load_dotenv()
    token = os.environ.get('ACCESS-TOKEN')

    # Создаем экземпляры классов
    vk = Api(token=token)
    gr = Graph()
    
    # Получаем ID пользователя
    try:
        user_id = int(input('Введите свой ID пользователя: '))
    except ValueError:
        raise ValueError('ID пользователя должен являться числом')
    
    # Получаем признак, по которому будет происходить группировка
    attribute = input('Введите признак, по которому будет строится граф: ')
    
    # Строим граф
    friends = vk.get_friends(user_id=user_id)
    gr.plot_graph(friends=friends, attribute=attribute)

