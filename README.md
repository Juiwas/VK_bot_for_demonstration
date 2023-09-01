Это ЧАСТЬ работы, которая была вырезана для демонстрации. 

# Bot_Vk_catboost
Это бот для ВК, классифицырующий сообщения через модель Catboost. 

В папке classification храняться сами модели  и модуль, отвечающий за работу с ними. 
Модели работают парно: модель-векторизатор. 

В папке Scenarios храняться все сценарии и доволнения к ним. Дополнения имеют то же название, что и сам сценарий. 

bot_catboost.py - главный файл 

bot_catboost_2.py - эксперементальный вариант. Пока в не рабочем состоянии


# __Файловая структура__


```

│   bot_catboost.py
│   bot_catboost_2.py
│   bot_vk.log
│   chats.py
│   create_bot.py
│   filials.py
│   meras.py
│   test.py
│   TOKEN.py
├───classification
│   │   __init__.py 
│   │   test_model.py
│   │   predobrabotka.py
│   │
│   ├───Models
│   │   │   __init__.py 
│   │   │   catboost_model_filifl_1
│   │   │   catboost_model_kakie_dokument
│   │   │   catboost_model_kogda_viplata
│   │   │   catboost_model_odobrenie
│   │   │   catboost_model_prodlenie
│   │   │   catboost_model_thanks_1
│   │   │   catboost_model_chto_poligeno
│   │   └───models.py
│   └───Vectorizers
│       │   ___init__.py vectorizer.pickle
│       │   py vectorizer.pickle
│       │   vectorizer_filifl_1.pickle
│       │   vectorizer_kakie_dokument.pickle
│       │   vectorizer_odobrenie
│       │   vectorizer_prodlenie.pickle
│       │   vectorizer_thanks_1.pickle
│       └───vectorizers.py
│
│
└───Scenarios
    │   chto_poligeno.py
    │   filiаl.py
    │   kakie_dokument.py
    │   kogda_viplata.py
    │   no_filial.py
    │   no_mera.py
    │   odobrenie.py
    │   prodlenie.py
    │   thank.py
    │   unified_manual.py
    │   __init__.py
    │
    ├───Menu
    │   │   menu_chto_poligeno.py
    │   │   menu_filiаl.py
    │   │   menu_kakie_dokument.py
    │   │   menu_kogda_viplata.py
    │   │   menu_odobrenie.py
    │   │   menu_prodlenie.py
    │   │   menu_thank.py
    │   │   menu_unified_manual.py
    │   └─── __init__.py
    │
    └───Mess
        │   mess_chto_poligeno.py
        │   mess_filiаl.py
        │   mess_kakie_dokument.py
        │   mess_kogda_viplata.py
        │   mess_odobrenie.py
        │   mess_prodlenie.py
        │   mess_thank.py
        │   mess_unified_manual.py
        │   number_EKC.py
        └─── __init__.py
```
=======


