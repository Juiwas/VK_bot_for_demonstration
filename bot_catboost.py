#!/usr/bin/env python3

#
#from mysettings import settings
#import mapiai
import logging
import sys

logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s:%(levelname)s:%(message)s',
        handlers = {
            logging.FileHandler('bot_vk.log'),
            logging.StreamHandler(sys.stdout)
            }
        )

logging.info(' Загрузка библиотек')

from vk_api.longpoll import VkEventType
from vk_api.utils import get_random_id
from vk_api.upload import VkUpload
import re
from pathlib import Path
from datetime import datetime

import time


from classification import classify_mera_and_tema, kakoi_filifl
from Scenarios import *
from create_bot import start_bot
from chats import create_new_chat, chek_time_mess


global user_dict
user_dict = dict()

logging.info(' Библиотеки загружены')


attachment_type = {'фото': 'photo',
                    'видеозапись': 'video',
                    'аудиозапись': 'audio',
                    'документ': 'doc',
                    'запись на стене': 'wall',
                    'товар': 'market',
                    'опрос': 'poll'
                    }



pattern = r'(?:0?[1-9]|[12][0-9]|3[01])-(?:0?[1-9]|1[0-2])-(?:19[0-9][0-9]|20[01][0-9])(?!\d)'
pattern2 = r'(?:0?[1-9]|[12][0-9]|3[01]).(?:0?[1-9]|1[0-2]).(?:19[0-9][0-9]|20[01][0-9])(?!\d)'


# Узнаем сейчас рабочее время или нет
def checking_working_time(now_time: int) -> bool:
    time = int(datetime.utcfromtimestamp(now_time).strftime('%H'))+5
    day = datetime.utcfromtimestamp(now_time).weekday()
    if day>=5: return False
    if time>=9 and time<18: return True
    else: return False
     

def time_msg(user_id: int, message: str):
    random_id=get_random_id()
    vk.method('utils.getServerTime') # отправляем сообщение


# Отправляет просто текстовое сообщение
def write_msg(user_id: int, message: str):
    """
    random_id - рандомное число. Надо для Вк
    user_id - id пользлвателя, которому отправляем сообщение
    message - само сообщение
    """ 
    random_id=get_random_id()
    vk.method('messages.send', {'user_id': user_id, 'message': message,'random_id':random_id}) # отправляем сообщение


# Отвечает на сообщение и отмечает его непрочитанным
def stop_msg(user_id: int, message: str, PEER_ID: int):
    """
    Отправляет сообщение пользователю. После чего отмечает непрочитанным.
    Что бы потом зашел оператор и сам на него ответил.

    random_id - рандомное число. Надо для Вк
    user_id - id пользлвателя, которому отправляем сообщение
    message - само сообщение
    PEER_ID - id чата с данным пользователем
    """    
    random_id=get_random_id()
    vk.method('messages.send', {'user_id': user_id, 'message': message,'random_id':random_id}) # отправляем сообщение
    vk.method('messages.markAsUnreadConversation', {'peer_id': PEER_ID}) # и отмечаем чат непрочитанным


# Без ответа чат отмечается прочитанным
def read_msg(user_id: int, PEER_ID: int):
    """
    PEER_ID - id чата с данным пользователем
    """ 
    vk.method('messages.markAsRead', {'peer_id': PEER_ID}) # Без ответа чат отмечается прочитанным


# Возвращает owner_id, photo_id, access_key для дальшейшей загрузки фото в сообщение функцией send_photo
def upload_photo(vk, photo)-> int:
    """
    Получает какой-то специальный api при уже нашем подключении. И сам подключается.
    Вытаскиваем путь к фото, что нам надо загрузить. 
    Он что-то с ним делает и мы получаем нужные ключи для дальшейшей работы. 

    vk - это наше подключение к API
    vk_s - это он что-то берет для подключения
    upload - а тут подключается
    file_photo - абсолютный путь фото
    response - только бог знает, что тут
    owner_id, photo_id, access_key - ключи, что нам нужны для работы
    """ 
    vk_s = vk.get_api()
    upload = VkUpload(vk_s)
    #берем родительский путь к данному файлу и добавляем файл, что нам нужен
    file_photo = str(myself.parents[0]) + '/' + photo 
    response = upload.photo_messages(file_photo)[0]

    owner_id = response['owner_id']
    photo_id = response['id']
    access_key = response['access_key']

    return owner_id, photo_id, access_key


# Отправляет сообщение с фото и текстом
def send_photo(vk, PEER_ID: int, message: str, owner_id: int, photo_id: int, access_key: str):
    """
    Приводит фото к нужному для отправке виду. 
    И отправляет в нужный чат по id чату сообщение с текстом и фото.

    attachment - фото в спец фиде лоя post запроса
    random_id - рандомное число. Надо для Вк
    message - само сообщение
    PEER_ID - id чата с данным пользователем
    """ 
    #attachment_type[фото]<owner_id>_<media_id>
    attachment = f'photo{owner_id}_{photo_id}_{access_key}'
    random_id=get_random_id()
    vk.method('messages.send', {'message': message,'random_id':random_id, 'peer_id': PEER_ID, 'attachment': attachment}) 



# обрабатываем полученное событие
def handle_events(vk, working_time: bool, event, user_dict: dict):
    if event.peer_id  != 2000000002: #если это не общий чат

        if event.type == VkEventType.MESSAGE_NEW:
  
            if not (event.user_id in user_dict): #если это новый чат (чата нет в нашей памяти)
                user_dict = create_new_chat(event.user_id, user_dict)
            user_dict[event.user_id]["peer_id"] = event.peer_id 
            user_dict[event.user_id]['time_last_mess'] = event.timestamp

            if user_dict[event.user_id]["messages_true"]==False: #Если на сообщения нельзя отвечать боту
                if event.to_me:
                    if "спасибо" in event.text.lower():
                        write_msg(event.user_id, "Рады были вам помочь!")
                        user_dict.pop(event.user_id, None) #удаляем из памяти этот чат
                        return 

                if not event.to_me: 
                    request = event.text.lower()
                    if ("рады были вам помочь" in request):  
                        user_dict.pop(event.user_id, None)  
                        return

            else: #Если на сообщения можно отвечать боту          
                if event.to_me: 
                    #print(event.__dict__)   
                    #print(event.raw)  
                    """
                    Люди могут прислать не только сообщение. Могут даже переслать сообщение.
                    Поэтому делаем проверку, что мы получили именно текстовое сообщение.
                    Пересланные сообщения пока не понятно как обрабатывать - вместо текта в ответе от сервера смайлик. 
                    """
                    if event.text == '': 
                        if 'fwd' in event.attachments:
                            write_msg(event.user_id, "Пожалуйста, не пересылайте сообщение, а напишите его заново. Или скопируйте и свтавьте. Иначе мы не сможем вам ответить.")
                        elif 'attach1_kind' in event.attachments and  event.attachments['attach1_kind']=='audiomsg':
                            write_msg(event.user_id, "Пожалуйста, напишите свой вопрос. Иначе я не смогу вам ответить.")
                        else:
                            write_msg(event.user_id, "Пожалуйста, напишите свой вопрос. Иначе я не смогу вам ответить.")
                        return

                    if "спасибо" in event.text.lower() and not ("заранее спасибо" in event.text.lower()):
                        write_msg(event.user_id, "Рады были вам помочь!")
                        user_dict.pop(event.user_id, None) 
                        return 
                    elif (event.text.lower().rstrip()=='здравствуйте' or 
                          event.text.lower().rstrip()=='добрый день' or 
                          event.text.lower().rstrip()=='здравствуйте!' or
                          event.text.lower().rstrip()=='начать'):
                        write_msg(event.user_id, "Здравствуйте! Какой у вас вопрос?")
                        return
                    elif event.text.lower().rstrip()=='?':
                        write_msg(event.user_id, "Какой у вас вопрос?")
                        return

   

                    # отпределяем тему и меру  
                    user_dict[event.user_id] = classify_mera_and_tema(event.text, user_dict, event.user_id)                     
                    #print(user_dict[event.user_id] if event.user_id == 163946274 else 'None')

                    if user_dict[event.user_id]['mera']=='Универсальное пособие': # универсальне отдельно обрабатываем, т.к. оно определяется как мера
                        if 'Универсальное пособие' not in user_dict[event.user_id].keys():
                            user_dict[event.user_id]["Универсальное пособие"] = {'check': True}
                        user_dict[event.user_id] = check_script_unified_manual(vk, event, user_dict)
                        if user_dict[event.user_id]['restart']:
                            user_dict[event.user_id]['restart'] = False
                            handle_events(vk, working_time, event, user_dict)

                    elif user_dict[event.user_id]['tema']!=None: # Мы уже знаем, какая тема
                        user_dict[event.user_id] = check_scenarios[user_dict[event.user_id]['tema']](vk, event, user_dict)
                        if user_dict[event.user_id]['restart']:
                            user_dict[event.user_id]['restart'] = False
                            handle_events(vk, working_time, event, user_dict)

                    else:  # если мы ещё не запустили никакой сценарий
                        if len(user_dict[event.user_id]['tema_c'])==1: # если определилась одна тема   

                            if user_dict[event.user_id]['tema_c'][0][2] and (user_dict[event.user_id]['filial']=='****' or user_dict[event.user_id]['filial']==None): #сценарию важн филиал    
                                check_script_no_filial(vk, event, user_dict)   
                                if user_dict[event.user_id]['restart']:
                                    user_dict[event.user_id]['restart'] = False
                                    handle_events(vk, working_time, event, user_dict)                     
                            elif user_dict[event.user_id]['tema_c'][0][1] and user_dict[event.user_id]['mera']=='****': #сценарию важна мера и у нас её нет
                                check_script_no_mera(vk, event, user_dict) 
                                user_dict[event.user_id]['mera']=None                          
                            else: #сценарию не важна мера или нам она важна и мы её знаем
                                user_dict[event.user_id][user_dict[event.user_id]['tema_c'][0][0]] = {'check': True}
                                user_dict[event.user_id] = check_scenarios[user_dict[event.user_id]['tema_c'][0][0]](vk, event, user_dict) 

                        elif len(user_dict[event.user_id]['tema_c'])==0: # не нашлась ни одна тема  
                            user_dict[event.user_id]["messages_true"]=False
                            if not working_time:
                                write_msg(event.user_id, 'Я не могу ответить на Ваш вопрос. Пожалуйста, дождитесь, когда начнется рабочий день операторов. Они придут и ответят на ваш вопрос. Спасибо за понимание.') 
                            vk.method('messages.markAsUnreadConversation', {'peer_id': event.user_id}) # и отмечаем чат непрочитанным
                        else: # если нашлось несколько тем
                            mess = """Возможно Вы задали несколько вопросов в одном.
                                      Пожалуйста, разделите свой вопрос."""
                            write_msg(event.user_id, mess) 











logging.info(' Бот запускается')
"""
vk, longpoll, now_time = start_bot()
while True:

    now_time_1 = vk.method('utils.getServerTime', {}) # получаем время на сервере
    working_time = checking_working_time(now_time_1) 
    if now_time_1 - now_time > 600:
        now_time = now_time_1
        user_dict, id_del = chek_time_mess(user_dict, now_time, vk)
        for id_d in id_del:
            pass
            #write_msg(id_d, "Вы были неактивные более 10 минут. Надеемся, мы вам помогли. Приятного дня.")
        logging.info('Запланированное переподключение') 
    events = longpoll.check()
    if len(events)>0: 
        for event in events:
            handle_events(vk, working_time, event, user_dict )    
    time.sleep(0.01)
"""

if __name__ == '__main__':
    # Основной цикл
    while True:
        try:
            now_time_1 = vk.method('utils.getServerTime', {}) # получаем время на сервере
            working_time = checking_working_time(now_time_1) 
            if now_time_1 - now_time > 600:
                now_time = now_time_1
                user_dict, id_del = chek_time_mess(user_dict, now_time, vk)
                for id_d in id_del:
                    pass
                    #write_msg(id_d, "Вы были неактивные более 10 минут. Надеемся, мы вам помогли. Приятного дня.")
                logging.info('Запланированное переподключение') 
            events = longpoll.check()
            if len(events)>0: 
                for event in events:
                    handle_events(vk, working_time, event, user_dict )    
            time.sleep(0.01)
        except KeyboardInterrupt as err:
            logging.info('Бот выключился')
            break
        except Exception as err:
            #raise err
            logging.error(err)
            logging.warning(' Бот остановился, следующая попытытка соединения через 2 секунд')
            t = True
            while t:
                time.sleep(2)
                try:
                    vk, longpoll, now_time = start_bot()
                except Exception as err:
                    logging.error(err)
                    logging.warning(' Бот остановился, следующая попытытка соединения через 2 секунд')
                else:
                    t = False
                    logging.info('Соединение востановлено')
                    now_time = vk.method('utils.getServerTime', {}) # получаем время на сервере


   
