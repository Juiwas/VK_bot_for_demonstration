"""
Сценарий для меры Универсальное пособие. Не зависит от темы. 

Меню и сам сценарий имеет такую иерархию:


"""
import vk_api
from vk_api.longpoll import VkEventType
from vk_api.utils import get_random_id
import re
from pathlib import Path

from Scenarios.Menu import chto_poligeno_menu
from Scenarios.Mess import chto_poligeno_mess


global name_scenario
name_scenario = "Опрос"

menu = 'Выберите пункт меню'

answer_0 = ['Нет', 'Ниже прожиточного минимума', 'Федеральная', 'Меньше 3']
answer_1 = ['Да', 'Выше прожиточного минимума', 'Региональная', '3 и более']

error_mes = "Повторите свой вопрос, пожалуйста."


#если ниже ПМ (прожиточный миниум)
next_question_N = {
	1: {0: 2, 1: [2, 'Почетный донор']},
	2: {0: 8, 1: [3]},
	3: {0: 10, 1: [4]},
	4: {0: 10, 1: [10, 'ЕДВ', 'Услуги связи']},
	5: {0: 10, 1: [3, 'МСП на оплату жилья и коммунальных услуг']},
	6: {0: 5, 1: [7, 'Пособие до 16(18) лет', 'Универсальное пособие']}, 
	7: {0: 9, 1: [9, 'ЕДВ на 3', 'РМК', 'Статус многодетной семьи', 'Школьная форма', 'Проезд многодетным']},
	8: {0: 6, 1: [6, 'Социальная степиндия']}, 
	9: {0: 10, 1: [10, 'областная ежеквартальная надбавка детям-инвалидам']},
	10: {0: None, 1: [None, 'Субсидия']}}

#если выше ПМ (прожиточный миниум)
next_question_V = {
	1: {0: 2, 1: [2, 'Почетный донор']},
	2: {0: 8, 1: [3]},
	3: {0: 6, 1: [4, 'МСП на оплату жилья и коммунальных услуг']},
	4: {0: 6, 1: [5, 'ЕДВ', 'Услуги связи']},
	5: {0: 6, 1: [6]},
	6: {0: None, 1: [7]}, 
	7: {0: 9, 1: [9, 'Статус многодетной семьи']},
	9: {0: None, 1: [None, 'областная ежеквартальная надбавка детям-инвалидам']},
}





def run_keyboard(vk, user_id: int, message: str, keyboard):
	"""
	random_id - рандомное число. Надо для Вк
	user_id - id пользлвателя, которому отправляем сообщение
	message - само сообщение
	""" 
	random_id=get_random_id()
	vk.method('messages.send', {'user_id': user_id, 'message': message ,'random_id':random_id, 'keyboard': keyboard.get_keyboard()}) # отправляем сообщение


def close_keyboard(vk, user_id: int, message: str, keyboard):
	random_id=get_random_id()
	vk.method('messages.send', {'user_id': user_id, 'message': message ,'random_id':random_id, 'keyboard': keyboard}) # отправляем сообщение

def close_scenario(user_dict: dict, event, messages_true):
    user_dict[event.user_id].pop(name_scenario, None) #закрываем сценарий
    user_dict[event.user_id]["messages_true"] = messages_true   
    user_dict[event.user_id]['tema'] = None 
    user_dict[event.user_id]['mera'] = None 
    return user_dict


def check_script_chto_poligeno(vk, event, user_dict: dict): 
	"""
    user_dict - слова пользователей
    event - произошедшее событие
    """ 
	if user_dict[event.user_id][name_scenario]['check']: # если первый запуск сценария
		user_dict[event.user_id]['tema'] = name_scenario
		user_dict[event.user_id][name_scenario]["question_now"] = 1 # добавляем запоминание уровня
		user_dict[event.user_id][name_scenario]['check'] = False 
		user_dict[event.user_id][name_scenario]['N_or_V'] = None # Если True - то выше прожиточного. Иначе ниже 
		user_dict[event.user_id][name_scenario]['answer'] = ''
		user_dict[event.user_id][name_scenario]['answer_now'] = None
		run_keyboard(vk, event.user_id, chto_poligeno_mess['question'][ user_dict[event.user_id][name_scenario]["question_now"] ],  chto_poligeno_menu[ user_dict[event.user_id][name_scenario]["question_now"] ])
	else:

		# для формирования ответа. Так же тут выясняем надо ли закрывать сценарий
		if event.text in answer_1:
			user_dict[event.user_id][name_scenario]['answer_now'] = 1
			if event.text=='Выше прожиточного минимума':  user_dict[event.user_id][name_scenario]['N_or_V'] = True 
		elif event.text in answer_0:  
			user_dict[event.user_id][name_scenario]['answer_now'] = 0
			if event.text=='Ниже прожиточного минимума':  user_dict[event.user_id][name_scenario]['N_or_V'] = False
		else: # не по сценарию
			user_dict = close_scenario(user_dict, event, True) #закрываем сценарий
			user_dict[event.user_id]['restart'] = True 
			return user_dict[event.user_id]	



		if user_dict[event.user_id][name_scenario]["question_now"] == 1: # если это был первый вопрос
			user_dict[event.user_id][name_scenario]["question_now"] = 2
			run_keyboard(vk, event.user_id, chto_poligeno_mess['question'][ user_dict[event.user_id][name_scenario]["question_now"] ],  chto_poligeno_menu[ user_dict[event.user_id][name_scenario]["question_now"] ])
		else: # уже остальные вопросы

			# от вети влияет какой дальше вопрос
			if user_dict[event.user_id][name_scenario]['N_or_V']: 
				user_dict[event.user_id][name_scenario]["question_now"] = next_question_V[user_dict[event.user_id][name_scenario]["question_now"]][user_dict[event.user_id][name_scenario]['answer_now']]
			else: 
			
				user_dict[event.user_id][name_scenario]["question_now"] = next_question_N[ user_dict[event.user_id][name_scenario]["question_now"]][user_dict[event.user_id][name_scenario]['answer_now'] ]

			if user_dict[event.user_id][name_scenario]['answer_now']==1: # если был дан положительный ответ
				if len(user_dict[event.user_id][name_scenario]["question_now"])!=1: # и надо добавить меру в ответ
					for i in user_dict[event.user_id][name_scenario]["question_now"][1:]: # ходим и добавляем
						user_dict[event.user_id][name_scenario]['answer'] += chto_poligeno_mess['answer'][i]
				user_dict[event.user_id][name_scenario]["question_now"] = user_dict[event.user_id][name_scenario]["question_now"][0]

			# если это конец, то выводим ответ. Иначе задаем дальше вопросы.
			if user_dict[event.user_id][name_scenario]["question_now"] == None:
				if user_dict[event.user_id][name_scenario]['answer']!='':
					close_keyboard(vk, event.user_id, chto_poligeno_mess['answer'][1]+user_dict[event.user_id][name_scenario]['answer'], chto_poligeno_menu[(0)])
				else:
					close_keyboard(vk, event.user_id, chto_poligeno_mess['answer'][0], chto_poligeno_menu[(0)])
				close_scenario(user_dict, event, True)
			else:
				run_keyboard(vk, event.user_id, chto_poligeno_mess['question'][ user_dict[event.user_id][name_scenario]["question_now"] ], chto_poligeno_menu[ user_dict[event.user_id][name_scenario]["question_now"] ])

	return user_dict[event.user_id]				
			 	



