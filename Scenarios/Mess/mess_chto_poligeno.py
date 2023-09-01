

question_0 = "Вы запустили опрос, дабы узнать, что вам может быть положено в ГКУ'ЦСПН'" + "\n" + "НИЧЕГО самостоятельно писать не надо. Только нажмите на кнопки. Если вы что-то напишите, то придется начинать опрос заново!" + "\n" + "\n"





question_1 = question_0 + """Вы имеете удостоверение почетного донора?"""

question_2 = """Доход на одного члена семьи"""

question_3 = """У вас имеется льготная категория?"""

question_4 = """Какая у вас льготная категория?"""

question_5 = """Вы достигли пенсионного возраста?"""

question_6 = """В семье есть дети?"""

question_7 = """Скольким из них меньше 18 лет??"""

question_8 = """Вы являетесь студентом?"""

question_9 = """В семье есть ребенок инвалид?"""

question_10 = """Вы являетесь собственником помещения проживания?"""



question = {1: question_1,
			2: question_2,
			3: question_3,
			4: question_4,
			5: question_5,
			6: question_6,
			7: question_7,
			8: question_8,
			9: question_9, 
			10: question_10,}


answer_0 = """В нашей организации никакая из мер поддержки вам не положена."""

answer_1 = """В ЦСПН вам положено:"""

answer_subsidia = "\n" +u"\U0001F539" + "Субсидия на оплату ЖКУ" + "\n" + "    Ссылка для подачи: " + 'https://www.gosuslugi.ru/600177/1/form'

answer_donor = "\n" +u"\U0001F539" + "Выплата почотному донору" + "\n" + "    Ссылка для подачи: " + "https://www.gosuslugi.ru/600200/2/info"

answer_edk = "\n" +u"\U0001F539" + "ЕДК" + "\n" + "    Ссылка для подачи: " + "https://www.gosuslugi.ru/600175/1/form"

answer_edv = "\n" +u"\U0001F539" + "ЕДВ"

answer_svas = "\n" +u"\U0001F539" + "Компенсация услуг связи" + "\n" + "    Ссылка для подачи: " + "https://www.gosuslugi.ru/600210/1/form"

answer_do_16 = "\n" +u"\U0001F539" + "Пособие до 16 лет" + "\n" + "    Ссылка для подачи: " + "https://www.gosuslugi.ru/600244/1/form"

answer_yniversal = "\n" +u"\U0001F539" + "Единое пособие в СФР"

answer_detam_invalidam = "\n" + u"\U0001F539" + "Обласная ежеквартальная надбавка детям-инвалидам " + "\n" + "    Ссылка для подачи: " +  "https://www.gosuslugi.ru/99930/2/form"

answer_forma = "\n" +u"\U0001F539" + "Компенсация школьной формы" 

answer_proezd = "\n" +u"\U0001F539" + "Компенсация проезда" 

answer_edv_na_3 = "\n" +u"\U0001F539" + "ЕДВ на 3 ребенка" + "\n" + "    Ссылка для подачи: " + "https://www.gosuslugi.ru/600198/1/form"

answer_status =  "\n" +u"\U0001F539" + "Статус многодетной семьи" + "\n" + "    Ссылка для подачи: " + "https://gosuslugi.ru/600164/1/form"

answer_rmk = "\n" +u"\U0001F539" + "Региональный материнский капитал" + "\n" + "    Ссылка для подачи: " + "https://www.gosuslugi.ru/600234/1/form" 

answer_stependi = "\n" +u"\U0001F539" + "Социальная степендия в учебном заведении" 



#если ниже ПМ
next_question_N = {
	1: {0: 2, 1: [2, answer_donor]},
	2: {0: 8, 1: [3]},
	3: {0: 10, 1: [4]},
	4: {0: 10, 1: [10, answer_edv, answer_svas]},
	5: {0: 10, 1: [3, answer_edk]},
	6: {0: 5, 1: [7, answer_do_16, answer_yniversal]}, 
	7: {0: 9, 1: [9, answer_edv_na_3, answer_rmk, answer_status, answer_forma, answer_proezd]},
	8: {0: 6, 1: [6, answer_stependi ]}, 
	9: {0: 10, 1: [10, answer_detam_invalidam]},
	10: {0: None, 1: [None, answer_subsidia]}}

#если выше ПМ
next_question_V = {
	1: {0: 2, 1: [2, answer_donor]},
	2: {0: 8, 1: [3]},
	3: {0: 6, 1: [4, answer_edk]},
	4: {0: 6, 1: [5, answer_edv, answer_svas]},
	5: {0: 6, 1: [6]},
	6: {0: None, 1: [7]}, 
	7: {0: 9, 1: [9, answer_status]},
	9: {0: None, 1: [None, answer_detam_invalidam]},
}





answer = {0: answer_0,
		  1: answer_1,
		  'Субсидия': answer_subsidia,
		  'Почетный донор': answer_donor,
		  'МСП на оплату жилья и коммунальных услуг': answer_edk,
		  'ЕДВ': answer_edv,
		  'Услуги связи': answer_svas,
		  'Пособие до 16(18) лет': answer_do_16,
		  'Универсальное пособие': answer_yniversal,
		  'областная ежеквартальная надбавка детям-инвалидам': answer_detam_invalidam,
		  'Школьная форма': answer_forma,
		  'Проезд многодетным': answer_proezd,
		  'ЕДВ на 3': answer_edv_na_3,
		  'Статус многодетной семьи': answer_status,
		  'РМК': answer_rmk,
		  'Социальная степендия': answer_stependi
		  }




chto_poligeno_mess = { 'question': question,
						'answer': answer	
						}

