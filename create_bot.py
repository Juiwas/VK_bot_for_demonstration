import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from datetime import datetime

from TOKEN import mytoken


	

# Подключение к Вк
def start_bot():
    vk = vk_api.VkApi(token=mytoken)
    # Работа с сообщениями
    longpoll = VkLongPoll(vk, wait=10)
    now_time = vk.method('utils.getServerTime', {}) # время на сервере

    return vk, longpoll, now_time 

