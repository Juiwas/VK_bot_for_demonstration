




def create_new_chat(user_id: int, user_dict: dict) -> dict:
    user_dict[user_id] = {
        "peer_id": None,
        "messages_true": True, # может ли бот отвечать на сообщение Да/Нет
        'mera': None, # какая мера сейчас обсуждается
        'tema': None, # какая тема сейчас обсуждается
        'tema_c': None, # тема сразу после классификации
        'tema_h': None, # тема, которую мы сохранили. Если нам для ответа что-то не хватает
        'time_last_mess': 0, # время последнего отправленого сообщения. Не важно пользователя или бота        
        'restart': False,  # флаг, показываеющий, что необходимо перезапустить обработчик
        'filial': None,
        }
    return user_dict



# Удаляем из памяти чаты, в которых не было активности более 10 минут
def chek_time_mess(user_dict: dict, now_time, vk) -> (dict, list):
    """
    Время в вк в секундах. Поэтому и разницу ищем в секундах
    id_del, list - добавляем id (peer_id) пользователей, которых удалим из чатов
    keys, list - id, которые есть у нас в памяти
    now_time, int - время на сервере в момент проверки 
    """
    id_del = []
    keys = list(user_dict.keys())
    for key in keys:
        if now_time - user_dict[key]['time_last_mess']>600:
            id_del.append(key)
            user_dict.pop(key, None) # удаляем чат из памяти   
    return user_dict, id_del          